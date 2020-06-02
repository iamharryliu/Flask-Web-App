from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

default_option = [(None, "Select")]

size_choices = [
    (None, "Select Size"),
    ("X-Small", "X-Small"),
    ("Small", "Small"),
    ("Medium", "Medium"),
    ("Large", "Large"),
    ("X-Large", "X-Large"),
]

quantity_choices = default_option + [(str(n), n) for n in range(1, 11)]


class ItemForm(FlaskForm):
    quantity = SelectField("Quantity", choices=quantity_choices)
    size = SelectField("Size", choices=size_choices)
    submit = SubmitField("Submit")
