import os
import json

# We want the database path to be in the main directory if we are using SQLite in order to work with Flask-Migrate.
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(DIR_PATH, os.pardir))

with open("/etc/config.json") as config_file:
    config = json.load(config_file)


class Config:

    SECRET_KEY = config.get("SECRET_KEY")
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{ROOT_PATH}/site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RECAPTCHA_USE_SSL = config.get("RECAPTCHA_USE_SSL")
    RECAPTCHA_PUBLIC_KEY = config.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = config.get("RECAPTCHA_PRIVATE_KEY")
    RECAPTCHA_OPTIONS = config.get("RECAPTCHA_OPTIONS")

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get("EMAIL_USERNAME")
    MAIL_PASSWORD = config.get("EMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = config.get("EMAIL_DEFAULT_SENDER")

    ADMINS = config.get("ADMINS")
