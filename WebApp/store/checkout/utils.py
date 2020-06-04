from flask import session, flash
from flask_login import current_user
from WebApp import db
from WebApp.models import Cart


def process_order():
    user = current_user
    cart = Cart(customer=user)
    db.session.add(cart)
    db.session.commit()
    send_order_email()


def send_order_email():
    pass
