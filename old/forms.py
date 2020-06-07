from flask import flash, request
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from datetime import date
import calendar


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
                pass
                # return result
            else:
                flash("Invalid date.", "danger")
                return False
