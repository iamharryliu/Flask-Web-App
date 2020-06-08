from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import current_user
from WebApp.main.forms import ContactForm
from WebApp.main.utils import handle_contact_message

main_blueprint = Blueprint("main", __name__, template_folder="templates")


@main_blueprint.route("/")
def home():
    return render_template("main/index.html", title="Home")


@main_blueprint.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        handle_contact_message()
        flash(f"Your message has been sent.", "success")
        return redirect(url_for("main.home"))
    return render_template("main/contact.html", title="Contact", form=form)


@main_blueprint.route("/subscribe_to_newsletter", methods=["POST"])
def subscribe_to_newsletter():
    email = request.form["email"]
    flash(f"You are now subscribed to the newsletter, {email}", "success")
    return redirect(request.referrer)
