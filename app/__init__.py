from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager

#initializes application
#sets configurations as specified in config.py
app = Flask(__name__)
app.config.from_object(Config)

#initializes database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#initializes login manager
login_manager = LoginManager()
login_manager.init_app(app)

#redirects user to login page if not logged in
login_manager.login_view = "login"

from app import routes
