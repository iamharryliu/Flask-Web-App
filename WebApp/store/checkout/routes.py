from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    request,
    session,
    flash,
    abort,
)
from flask_login import login_required, current_user
from WebApp.store.cart.utils import update_cart_values
from WebApp.store.checkout.forms import AddressForm, CreditCardForm, CheckoutForm
from WebApp.store.cart.utils import get_user_cart, get_user_cart_and_items
from WebApp.store.checkout.utils import (
    add_address,
    get_user_addresses,
    get_address,
    edit_address,
    set_default_address,
    update_address_form,
    delete_address,
    add_card,
    get_cards,
    get_card,
    get_filled_card_form,
    edit_card,
    set_default_card,
    delete_card,
    process_order,
)
from datetime import datetime

checkout_blueprint = Blueprint(
    "checkout_blueprint",
    __name__,
    url_prefix="/store/checkout",
    template_folder="templates",
)


@checkout_blueprint.route("", methods=["GET", "POST"])
def address():
    # update_cart_values()
    form = CheckoutForm()
    # cart = get_user_cart()
    if form.validate_on_submit():
        flash("successful", "success")
        return redirect(url_for("checkout_blueprint.address"))
    return render_template("checkout.html", title="Checkout", form=form)


@checkout_blueprint.route(
    "/checkout/address/<path:subpath>/add", methods=["GET", "POST"]
)
@login_required
def add_address_route(subpath):
    form = AddressForm()
    if form.validate_on_submit():
        add_address()
        return redirect(url_for("checkout_blueprint.address", subpath=subpath))
    cart = get_user_cart()
    return render_template(
        "checkout/address/components/add-edit-address/view.html",
        cart=cart,
        subpath=subpath,
        form=form,
    )


@checkout_blueprint.route(
    "/<path:subpath>/<int:address_id>/edit", methods=["GET", "POST"]
)
@login_required
def edit_address_route(subpath, address_id):
    address = get_address(address_id)
    if address.customer != current_user:
        abort(400)
    form = AddressForm()
    if form.validate_on_submit():
        edit_address(address)
        return redirect(url_for("checkout_blueprint.address", subpath=subpath))
    form = update_address_form(address)
    cart = get_user_cart()
    return render_template(
        "checkout/address/components/add-edit-address/view.html",
        subpath=subpath,
        cart=cart,
        form=form,
        address=address,
    )


@checkout_blueprint.route("/<path:subpath>/default/<int:address_id>/", methods=["POST"])
@login_required
def set_default_address_route(subpath, address_id):
    set_default_address(address_id)
    return redirect(url_for("checkout_blueprint.address", subpath=subpath))


@checkout_blueprint.route("/<path:subpath>/delete/<int:address_id>/", methods=["POST"])
@login_required
def checkout_address_delete(subpath, address_id):
    delete_address(address_id)
    return redirect(url_for("checkout_blueprint.address", subpath=subpath))


@checkout_blueprint.route("/<path:subpath>/submit", methods=["POST"])
@login_required
def submit_address(subpath):
    address = request.form.get("addresses")
    if address:
        session[subpath] = address
        route = get_submit_address_route(subpath)
        return route
    else:
        flash("Please select an address. If no addresses exist add them.", "danger")
        return redirect(url_for("checkout_blueprint.address", subpath=subpath))


def get_submit_address_route(subpath):
    if subpath == "shipping_address":
        return redirect(url_for("checkout_blueprint.shipping_option"))
    else:
        return redirect(url_for("checkout_blueprint.payment"))


# Shipping Option


@checkout_blueprint.route("/shipping_option", methods=["GET"])
@login_required
def shipping_option():
    update_cart_values()
    if session["shipping_address"] == None:
        abort(400)
    cart = get_user_cart()
    return render_template(
        "checkout/shipping-option/view.html", title="Shipping Option", cart=cart
    )


@checkout_blueprint.route("/shipping_option/submit", methods=["POST"])
@login_required
def submit_shipping_option():
    update_cart_values()
    shipping_option = request.form.get("shipping_options")
    if shipping_option:
        session["shipping_option"] = shipping_option
        return redirect(
            url_for("checkout_blueprint.address", subpath="billing_address")
        )
    return redirect(url_for("checkout_blueprint.shipping_option"))


# Payment


@checkout_blueprint.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    update_cart_values()
    if session["billing_address"] == None:
        abort(400)
    cards = get_cards()
    cart = get_user_cart()
    date_now = datetime.now()
    return render_template(
        "checkout/payment/view.html",
        title="Payment",
        cards=cards,
        cart=cart,
        date_now=date_now,
    )


@checkout_blueprint.route("/add_payment_method", methods=["GET", "POST"])
@login_required
def add_payment_route():
    form = CreditCardForm()
    if form.validate_on_submit():
        add_card()
        return redirect(url_for("checkout_blueprint.payment"))
    else:
        pass
    cart = get_user_cart()
    return render_template(
        "checkout/payment/components/add-edit-payment/view.html",
        title="Payment",
        cart=cart,
        form=form,
    )


@checkout_blueprint.route("/payment/edit/<int:card_id>", methods=["GET", "POST"])
@login_required
def edit_card_route(card_id):
    card = get_card(card_id)
    if card.owner != current_user:
        abort(400)
    form = CreditCardForm()
    if form.validate_on_submit():
        edit_card(card)
        return redirect(url_for("checkout_blueprint.payment"))
    form = get_filled_card_form(card)
    cart = get_user_cart()
    return render_template(
        "checkout/payment/components/add-edit-payment/view.html",
        title="Payment",
        cart=cart,
        form=form,
        address=address,
    )


@checkout_blueprint.route("/payment/default/<int:card_id>/", methods=["POST"])
@login_required
def set_default_payment_route(card_id):
    set_default_card(card_id)
    return redirect(url_for("checkout_blueprint.payment"))


@checkout_blueprint.route("/delete_card/<int:card_id>/", methods=["POST"])
@login_required
def delete_card_route(card_id):
    delete_card(card_id)
    return redirect(url_for("checkout_blueprint.payment"))


@checkout_blueprint.route("/payment/submit", methods=["POST"])
@login_required
def submit_payment():
    card_id = request.form.get("card_id")
    if card_id:
        session["payment"] = card_id
        return redirect(url_for("checkout_blueprint.review"))
    else:
        flash("A payment option must be selected.", "danger")
        return redirect(url_for("checkout_blueprint.payment"))


# Review Order


@checkout_blueprint.route("/review", methods=["GET", "POST"])
@login_required
def review():
    update_cart_values()
    if session["payment"] == None:
        abort(400)
    if request.method == "POST":
        process_order()
        return render_template("checkout/successful-order/view.html")
    cart, cart_items = get_user_cart_and_items()
    order_details = {
        "shipping_address": get_address(session["shipping_address"]),
        "shipping_option": session["shipping_option"],
        "billing_address": get_address(session["billing_address"]),
    }
    return render_template(
        "checkout/review/view.html",
        title="Review",
        cart=cart,
        cart_items=cart_items,
        order_details=order_details,
        session=session,
    )
