from flask import session, request
from flask_login import current_user
from WebApp import db
from WebApp.models import Cart, CartItem
from WebApp.store.products.forms import ItemForm


import random, string


# Create


def add_item_to_cart(product):
    if current_user.is_authenticated:
        add_item_to_user_cart(product)
    else:
        add_item_to_anonymous_cart(product)


def add_item_to_user_cart(product):
    form = ItemForm()
    cart = get_user_cart()
    cart_item = (
        CartItem.query.filter_by(cart_id=cart.id)
        .filter_by(product_id=product.id)
        .filter_by(size=form.size.data)
        .first()
    )
    if cart_item:
        cart_item.quantity = form.quantity.data
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=form.quantity.data,
            size=form.size.data,
        )
        db.session.add(cart_item)
    db.session.commit()


def add_item_to_anonymous_cart(product):
    form = ItemForm()
    quantity = form.quantity.data
    size = form.size.data
    session["cart"]["cart_items"].append(
        {
            "product": {
                "name": product.name,
                "code": product.code,
                "color": product.color,
                "image_file": product.image_file,
                "price": product.price,
                "description": product.description,
            },
            "quantity": int(quantity),
            "size": size,
            "id": "".join(
                [random.choice(string.ascii_letters + string.digits) for n in range(32)]
            ),
        }
    )


# Read


def get_user_cart():
    cart = (
        Cart.query.filter_by(customer=current_user)
        .order_by(Cart.id.desc())
        .first_or_404()
    )
    return cart


def get_cart_items(cart):
    items = CartItem.query.filter_by(cart_id=cart.id)
    return items


def get_user_cart_and_items():
    cart = get_user_cart()
    items = get_cart_items(cart).order_by(CartItem.id.desc()).all()
    return cart, items


def get_cart_item(id):
    item = CartItem.query.filter_by(id=id).first_or_404()
    return item


# Update


def update_cart_items():
    cart = get_user_cart()
    items = get_cart_items(cart).order_by(CartItem.id.desc()).all()
    ids = request.form.keys()
    for _id in ids:
        for item in items:
            if item.id == int(_id):
                item.quantity = int(int(request.form[_id]))
    db.session.commit()


def update_cart_item(item):
    form = ItemForm()
    item.quantity = int(form.quantity.data)
    item.size = form.size.data
    db.session.commit()


def update_cart_values():
    cart, cart_items = get_user_cart_and_items()
    cart.total = 0
    cart.quantity = 0
    for item in cart_items:
        cart.total += item.product.price * float(item.quantity)
        cart.quantity += item.quantity
    db.session.commit()


# Delete


def delete_cart_item(cart_item):
    db.session.delete(cart_item)
    cart = get_user_cart()
    db.session.commit()


def delete_all_cart_items():
    cart = get_user_cart()
    cartItems = get_cart_items(cart=cart)
    cartItems.delete()
    db.session.commit()
