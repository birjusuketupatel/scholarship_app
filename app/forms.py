from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import User
from app import db

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")

    #checks that given email is in database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("invalid email")

    #checks password matches given email
    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()

        if user is None:
            return

        if not user.check_password(password.data):
            raise ValidationError("invalid password")
