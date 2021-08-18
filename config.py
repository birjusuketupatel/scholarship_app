import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    #for secure form input
    SECRET_KEY = os.environ.get("SECRET_KEY") or "my_secret"

    #configure sqlite database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #configures email server
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")

    #google recaptcha integration
    SECRET_KEY = os.environ.get("SECRET_KEY") or "my_secret"
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = "6LebLAkcAAAAAOlWkbZ20xXx1Cspwqdrc8pHswVh"
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
