from flask import Blueprint, render_template, url_for, redirect, session, flash
from flask_login import login_required, current_user
from WebApp.store.checkout.forms import CheckoutForm
from WebApp.store.checkout.utils import process_order
from WebApp.models import Order
from WebApp import db

checkout_blueprint = Blueprint(
    "checkout_blueprint", __name__, url_prefix="/checkout", template_folder="templates"
)


@checkout_blueprint.route("", methods=["GET", "POST"])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():

        flash("success", "success")

        newsletter_sub = form.newsletter_sub.data
        order = Order(
            email=form.email.data,
            shipping_first_name=form.shipping_first_name.data,
            shipping_last_name=form.shipping_last_name.data,
            shipping_address=form.shipping_address.data,
            shipping_address_unit=form.shipping_address_unit.data,
            shipping_city=form.shipping_city.data,
            shipping_region=form.shipping_region.data,
            shipping_country=form.shipping_country.data,
            shipping_postal_code=form.shipping_postal_code.data,
            shipping_phone_number=form.shipping_phone_number.data,
            shipping_method=form.shipping_method.data,
            card_number=form.card_number.data,
            card_name=form.card_name.data,
            card_expiration_month=form.card_expiration_month.data,
            card_expiration_year=form.card_expiration_year.data,
            billing_first_name=form.billing_first_name.data,
            billing_last_name=form.billing_last_name.data,
            billing_address=form.billing_address.data,
            billing_address_unit=form.billing_address_unit.data,
            billing_city=form.billing_city.data,
            billing_region=form.billing_region.data,
            billing_country=form.billing_country.data,
            billing_postal_code=form.billing_postal_code.data,
            billing_phone_number=form.billing_phone_number.data,
        )
        if current_user.is_authenticated:
            order.customer = current_user
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("checkout_blueprint.checkout"))
    return render_template("checkout.html", title="Checkout", form=form)
