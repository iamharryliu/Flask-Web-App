from flask import (
    Blueprint,
    render_template,
    request,
    session,
    abort,
    redirect,
    url_for,
    flash,
)
from flask_login import login_required, current_user
from WebApp.models import Cart
from WebApp.store.forms import ItemForm
from WebApp.store.utils import (
    get_cart_and_cart_item_with_total_and_quantity,
    get_cart_item_and_form,
    get_list_of_cart_items,
    update_cart_items,
    update_cart_item,
    delete_cart_item,
    delete_all_cart_items,
)


cart_blueprint = Blueprint(
    "cart_blueprint", __name__, url_prefix="/cart", template_folder="templates"
)


@cart_blueprint.route("")
def cart():
    cart, cart_items = get_cart_and_cart_item_with_total_and_quantity()
    return render_template(
        "cart/view.html", title="Cart", cart=cart, cart_items=cart_items
    )


@cart_blueprint.route("/update", methods=["POST"])
def cart_update():
    update_cart_items()
    return redirect(url_for("cart_blueprint.cart"))


@cart_blueprint.route("/<item_id>", methods=["GET", "POST"])
def cart_item_update(item_id):
    item, form = get_cart_item_and_form(item_id)
    if form.validate_on_submit():
        update_cart_item(item)
        return redirect(url_for("cart_blueprint.cart"))
    return render_template(
        "products/product-item.html", title="Edit Cart Item", item=item, form=form
    )


@cart_blueprint.route("/<item_id>/delete", methods=["POST"])
def cart_delete_item(item_id):
    delete_cart_item(item_id)
    return redirect(url_for("cart_blueprint.cart"))


@cart_blueprint.route("/clear", methods=["POST"])
def cart_clear():
    delete_all_cart_items()
    return redirect(url_for("cart_blueprint.cart"))


@cart_blueprint.route("/submit", methods=["POST"])
def submit_cart():
    cart_items = get_list_of_cart_items()
    if cart_items:
        return redirect(url_for("checkout.checkout"))
    else:
        flash("Add items to cart to checkout.", "danger")
        return redirect(url_for("cart_blueprint.cart"))
