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

from WebApp.store.products.forms import ItemForm
from WebApp.models import Cart
from WebApp.store.cart.utils import (
    get_list_of_cart_items,
    get_cart_item,
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
    if current_user.is_authenticated:
        cart = current_user.carts[0]
        cart_items = get_list_of_cart_items()
        cart.total = 0
        cart.quantity = 0
        for item in cart_items:
            cart.total += item.product.price * float(item.quantity)
            cart.quantity += item.quantity
    else:
        cart = session["cart"]
        cart_items = cart["cart_items"]
        cart_total = 0
        cart_quantity = 0
        for item in cart_items:
            cart_total += item["quantity"] * item["product"]["price"]
            cart_quantity += item["quantity"]
        cart["total"] = cart_total
        cart["quantity"] = cart_quantity
    return render_template(
        "cart/view.html", title="Cart", cart=cart, cart_items=cart_items
    )


@cart_blueprint.route("/update", methods=["POST"])
def cart_update():
    update_cart_items()
    return redirect(url_for("cart_blueprint.cart"))


@cart_blueprint.route("/<item_id>", methods=["GET", "POST"])
def cart_item_update(item_id):
    form = ItemForm()
    if current_user.is_authenticated:
        item = get_cart_item(item_id)
        if form.validate_on_submit():
            update_cart_item(item)
            return redirect(url_for("cart_blueprint.cart"))
        form.quantity.data = str(item.quantity)
        form.size.data = item.size
        product = item.product
    else:
        item = next(
            (item for item in session["cart"]["cart_items"] if item["id"] == item_id),
            None,
        )
        if form.validate_on_submit():
            item["quantity"] = int(form.quantity.data)
            item["size"] = form.size.data
            session["cart"]["cart_items"][:] = [
                item for item in session["cart"]["cart_items"] if item["id"] != item_id
            ]
            session["cart"]["cart_items"].append(item)
            return redirect(url_for("cart_blueprint.cart"))
        form.quantity.data = str(item["quantity"])
        form.size.data = item["size"]
        product = item["product"]
    return render_template(
        "products/product-item.html", title="Edit Cart Item", product=product, form=form
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
        return redirect(url_for("checkout_blueprint.checkout"))
    else:
        flash("Add items to cart to checkout.", "danger")
        return redirect(url_for("cart_blueprint.cart"))
