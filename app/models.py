from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#table of users
#inherits UserMixin, contains default implementatios
#of methods required by LoginManager
class User(UserMixin, db.Model):
    #columns in table
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    #gets user id
    #required by LoginManager
    def get_id(self):
           return (self.user_id)

    #password is stored as hash for security
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, 'pbkdf2:sha256', 16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User user_id={}, email={}>".format(self.user_id, self.email)

#gets user given id
#required by LoginManager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
