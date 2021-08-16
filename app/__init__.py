from flask import Flask
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

from app import routes
