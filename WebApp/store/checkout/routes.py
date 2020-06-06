from flask import Blueprint, render_template, url_for, redirect, flash, request, abort
from flask_login import login_required, current_user
from WebApp.store.forms import CheckoutForm
from WebApp.store.utils import process_order

checkout_blueprint = Blueprint(
    "checkout_blueprint", __name__, url_prefix="/checkout", template_folder="templates"
)


@checkout_blueprint.route("", methods=["GET", "POST"])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        process_order()
        flash("Order has been processsed.", "success")
        return redirect(url_for("checkout_blueprint.checkout_success"))
    return render_template("checkout.html", title="Checkout", form=form)


@checkout_blueprint.route("/success")
def checkout_success():
    if request.referrer:
        return render_template("checkout_success.html", title="Checkout")
    else:
        abort(400)
