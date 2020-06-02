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
from WebApp.store.products.forms import ItemForm
from WebApp.models import Cart
from WebApp.store.cart.utils import (
    get_user_cart,
    get_cart_items,
    get_user_cart_and_items,
    get_cart_item,
    update_cart_items,
    update_cart_item,
    delete_cart_item,
    delete_all_cart_items,
)


cart_blueprint = Blueprint(
    "cart_blueprint", __name__, url_prefix="/store/cart", template_folder="templates"
)


@cart_blueprint.route("")
def cart():
    if current_user.is_authenticated:
        cart = get_user_cart()
        cart_items = get_cart_items(cart)
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
    if current_user.is_authenticated:
        update_cart_items()
    else:
        ids = request.form.keys()
        for _id in ids:
            for item in session["cart"]["cart_items"]:
                if item["id"] == _id:
                    item["quantity"] = int(request.form[item["id"]])
    return redirect(url_for("cart_blueprint.cart"))


@cart_blueprint.route("/<item_id>", methods=["GET", "POST"])
def cart_item_edit(item_id):
    form = ItemForm()
    if current_user.is_authenticated:
        item = get_cart_item(item_id)
        cart = Cart.query.get(item.cart_id)
        if cart.customer != current_user:
            abort(403)
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
    if current_user.is_authenticated:
        cart_item = get_cart_item(item_id)
        cart = cart_item.cart
        if cart.customer != current_user:
            abort(403)
        delete_cart_item(cart_item)
    else:
        print(item_id)
        session["cart"]["cart_items"] = [
            item for item in session["cart"]["cart_items"] if item["id"] != item_id
        ]

    return redirect(url_for("cart_blueprint.cart"))


@cart_blueprint.route("/clear", methods=["POST"])
def cart_clear():
    if current_user.is_authenticated:
        delete_all_cart_items()
    else:
        session["cart"]["cart_items"] = []
    return redirect(url_for("cart_blueprint.cart"))


@cart_blueprint.route("/submit", methods=["POST"])
def submit_cart():
    if current_user.is_authenticated:
        cart = get_user_cart()
        cart_items = cart.cart_items
    else:
        cart_items = session["cart"]["cart_items"]
    if cart_items:
        return redirect(url_for("checkout_blueprint.address"))
    else:
        flash("Add items to cart to checkout.", "danger")
        return redirect(url_for("cart_blueprint.cart"))
