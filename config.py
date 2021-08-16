import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY") or "bd\x9ck{\xb5\xd0D\x84\xbc\xb5[\xb8r_\x85\xf2~\xd9\xf8zi\xa1\xd4\xe4d"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
