from flask import session, flash
from flask_login import current_user
from WebApp import db
from WebApp.models import CheckoutAddress, Cart, CreditCard
from WebApp.store.checkout.forms import AddressForm, CreditCardForm

from datetime import date
import calendar

"""
Address functions
"""

# Create


def add_address():
    form = AddressForm()
    email = form.email.data
    phone = form.phone.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    address = form.address.data
    apartment = form.apartment.data
    city = form.city.data
    province = form.province.data
    country = form.country.data
    postal_code = form.postal_code.data
    checkout_address = CheckoutAddress(
        customer=current_user,
        email=email,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        address=address,
        apartment=apartment,
        city=city,
        province=province,
        country=country,
        postal_code=postal_code,
    )
    db.session.add(checkout_address)
    db.session.commit()


# Read


def get_user_addresses(user):
    addresses = (
        CheckoutAddress.query.order_by(CheckoutAddress.default.desc())
        .filter_by(customer=user)
        .all()
    )
    return addresses


def get_address(id):
    address = CheckoutAddress.query.get(id)
    return address


def getDefaultAddress():
    address = (
        CheckoutAddress.query.filter_by(customer=current_user)
        .filter_by(default=True)
        .first()
    )
    return address


# Update


def update_address_form(address):
    form = AddressForm()
    form.email.data = address.email
    form.phone.data = address.phone
    form.first_name.data = address.first_name
    form.last_name.data = address.last_name
    form.address.data = address.address
    form.apartment.data = address.apartment
    form.city.data = address.city
    form.province.data = address.province
    form.country.data = address.country
    form.postal_code.data = address.postal_code
    return form


def edit_address(address):
    form = AddressForm()
    address.email = form.email.data
    address.phone = form.phone.data
    address.first_name = form.first_name.data
    address.last_name = form.last_name.data
    address.address = form.address.data
    address.apartment = form.apartment.data
    address.city = form.city.data
    address.province = form.province.data
    address.country = form.country.data
    address.postal_code = form.postal_code.data
    db.session.commit()


def set_default_address(address_id):
    unset_default_address()
    address = get_address(address_id)
    address.default = True
    db.session.commit()


def unset_default_address():
    address = getDefaultAddress()
    if address:
        address.default = False
        db.session.commit()


# Delete


def delete_address(address_id):
    address = get_address(address_id)
    db.session.delete(address)
    db.session.commit()


# Create


def add_card():
    form = CreditCardForm()
    number = form.number.data
    name = form.name.data
    expiration_month = form.expiration_month.data
    expiration_year = form.expiration_year.data
    expiration_day = calendar.monthrange(int(expiration_year), int(expiration_month))[1]
    expiration_date = date(int(expiration_year), int(expiration_month), expiration_day)
    credit_card = CreditCard(
        owner=current_user,
        number=number,
        name=name,
        expiration_date=expiration_date,
        expiration_month=expiration_month,
        expiration_year=expiration_year,
    )
    db.session.add(credit_card)
    db.session.commit()
    flash("Payment successfully added", "success")


# Read


def get_cards():
    cards = CreditCard.query.filter_by(owner=current_user).all()
    return cards


def get_card(id):
    card = CreditCard.query.get(id)
    return card


def get_filled_card_form(card):
    form = CreditCardForm()
    form.number.data = card.number
    form.name.data = card.name
    form.expiration_month.data = card.expiration_month
    form.expiration_year.data = card.expiration_year
    return form


def get_default_card():
    address = (
        CreditCard.query.filter_by(owner=current_user).filter_by(default=True).first()
    )
    return address


# Update


def edit_card(card):
    form = CreditCardForm()
    card.number = form.number.data
    card.name = form.name.data
    card.expiration_month = form.expiration_month.data
    card.expiration_year = form.expiration_year.data
    db.session.commit()


def set_default_card(card_id):
    unset_default_card()
    card = get_card(card_id)
    card.default = True
    db.session.commit()


def unset_default_card():
    card = get_default_card()
    if card:
        card.default = False
        db.session.commit()


# Delete


def delete_card(card_id):
    card = CreditCard.query.get(card_id)
    db.session.delete(card)
    db.session.commit()
    flash("Payment successfully deleted.", "success")


# Other


def process_order():
    user = current_user
    cart = Cart(customer=user)
    db.session.add(cart)
    db.session.commit()
    send_order_email()


def send_order_email():
    pass
