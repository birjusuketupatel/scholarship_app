import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    #for secure form input
    SECRET_KEY = os.environ.get("SECRET_KEY") or "bd\x9ck{\xb5\xd0D\x84\xbc\xb5[\xb8r_\x85\xf2~\xd9\xf8zi\xa1\xd4\xe4d"

    #configure sqlite database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #configures email server
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = "birju.noreply@gmail.com"
    MAIL_PASSWORD = "<w88#5%h3/]CjyX\\"
    MAIL_DEFAULT_SENDER = "birju.noreply@gmail.com"

    #google recaptcha integration
    SECRET_KEY = "bd\x9ck{\xb5\xd0D\x84\xbc\xb5[\xb8r_\x85\xf2~\xd9\xf8zi\xa1\xd4\xe4d"
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = "6LebLAkcAAAAAOlWkbZ20xXx1Cspwqdrc8pHswVh"
    RECAPTCHA_PRIVATE_KEY = "6LebLAkcAAAAAAObCznbFwq1q_rfUjahkoYaYvz9"
