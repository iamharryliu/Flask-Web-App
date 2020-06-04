from flask import flash, request
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
    DateField,
    RadioField,
    BooleanField,
)
from wtforms.validators import DataRequired, Email, ValidationError
from datetime import date
import calendar

provinces = [
    ("--", "--"),
    ("Alberta", "AB"),
    ("British Columbia", "BC"),
    ("Manitoba", "MB"),
    ("New Brunswich", "NB"),
    ("Newfoundland and Labrador", "NL"),
    ("Northwest Territories", "NT"),
    ("Nova Scotia", "NS"),
    ("Nunavat", "NU"),
    ("Ontario", "ON"),
    ("Prince Edward Island", "PEI"),
    ("Quebec", "QC"),
    ("Saskatchewan", "SK"),
    ("Yukon", "YT"),
]

countries = [("--", "--"), ("Canada", "CA")]


class CheckoutForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    newsletter_sub = BooleanField(
        "Keep me up to date on news and exclusive offers", default=True
    )
    shipping_first_name = StringField("First Name", validators=[DataRequired()])
    shipping_last_name = StringField("Last Name", validators=[DataRequired()])
    shipping_address = StringField("Address", validators=[DataRequired()])
    shipping_address_unit = StringField("Apartment")
    shipping_city = StringField("City", validators=[DataRequired()])
    shipping_region = SelectField(
        "State/Province/Region",
        choices=provinces,
        default="--",
        validators=[DataRequired()],
    )
    shipping_postal_code = StringField("Postal Code", validators=[DataRequired()])
    shipping_country = SelectField(
        "Country", choices=countries, default="--", validators=[DataRequired()]
    )
    shipping_phone_number = StringField("Phone Number", validators=[DataRequired()])

    shipping_method = RadioField(
        "Shipping Method",
        choices=[
            ("Standard", "Standard ( 7 - 14 Business Days )"),
            ("Express", "Express ( 1 - 7 Business Days"),
        ],
        validators=[DataRequired()],
        default="Standard",
    )

    card_number = StringField("Card Number", validators=[DataRequired()])
    card_name = StringField("Name on Card", validators=[DataRequired()])
    card_expiration_month = StringField("Exp. Month", validators=[DataRequired()])
    card_expiration_year = StringField("Exp. Year", validators=[DataRequired()])

    same_as_shipping = BooleanField("Same as shipping addess")

    billing_first_name = StringField("First Name", validators=[DataRequired()])
    billing_last_name = StringField("Last Name", validators=[DataRequired()])
    billing_address = StringField("Address", validators=[DataRequired()])
    billing_address_unit = StringField("Apartment")
    billing_city = StringField("City", validators=[DataRequired()])
    billing_region = SelectField(
        "State/Province/Region", choices=provinces, default="--"
    )
    billing_postal_code = StringField("Postal Code", validators=[DataRequired()])
    billing_country = SelectField("Country", choices=countries, default="--")
    billing_phone_number = StringField("Phone Number", validators=[DataRequired()])

    submit = SubmitField("Submit")


class CreditCardForm(FlaskForm):
    def validate_on_submit(self):
        if request.method == "POST":
            expiration_month = int(self.expiration_month.data)
            expiration_year = int(self.expiration_year.data)
            expiration_day = calendar.monthrange(expiration_year, expiration_month)[1]
            expiration_date = date(expiration_year, expiration_month, expiration_day)
            # result = super(CreditCardForm, self).validate()
            today = date.today()
            if expiration_date > today:
                return result
            else:
                flash("Invalid date.", "danger")
                return False
