from flask import session, request
from flask_login import current_user
from WebApp import db
from WebApp.models import Cart, Item
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
    cart = current_user.carts[0]
    cart_item = (
        Item.query.filter_by(cart_id=cart.id)
        .filter_by(product_id=product.id)
        .filter_by(size=form.size.data)
        .first()
    )
    if cart_item:
        cart_item.quantity = form.quantity.data
    else:
        cart_item = Item(
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


def get_cart_items_query():
    cart = current_user.carts[0]
    return Item.query.filter_by(cart_id=cart.id)


def get_list_of_cart_items():
    if current_user.is_authenticated:
        items = get_cart_items_query()
    else:
        items = session["cart"]["cart_items"]
    return items.all()


def get_cart_item(id):
    return Item.query.filter_by(id=id).first_or_404()


# Update


def update_cart_items():
    if current_user.is_authenticated:
        items = get_cart_items_query().order_by(Item.id.desc()).all()
        ids = request.form.keys()
        for _id in ids:
            for item in items:
                if item.id == int(_id):
                    item.quantity = int(int(request.form[_id]))
        db.session.commit()
    else:
        ids = request.form.keys()
        for _id in ids:
            for item in session["cart"]["cart_items"]:
                if item["id"] == _id:
                    item["quantity"] = int(request.form[item["id"]])


def update_cart_item(item):
    form = ItemForm()
    item.quantity = int(form.quantity.data)
    item.size = form.size.data
    db.session.commit()


def update_cart_values():
    items = get_list_of_cart_items()
    cart.total = 0
    cart.quantity = 0
    for item in items:
        cart.total += item.product.price * float(item.quantity)
        cart.quantity += item.quantity
    db.session.commit()


# Delete


def delete_cart_item(item_id):
    if current_user.is_authenticated:
        item = get_cart_item(item_id)
        db.session.delete(item)
        db.session.commit()
    else:
        items = session["cart"]["cart_items"]
        session["cart"]["cart_items"] = [
            item for item in items if item["id"] != item_id
        ]


def delete_all_cart_items():
    if current_user.is_authenticated:
        cart_items = get_cart_items_query()
        cart_items.delete()
        db.session.commit()
    else:
        session["cart"]["cart_items"] = []


def delete_all_cart_items_anon():
    session["cart"]["cart_items"] = []
