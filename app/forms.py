from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms.widgets import PasswordInput
from app.models import User
from app import db

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")

    #checks that given email is in database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Invalid email.")

    #checks password matches given email
    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()

        if user is None:
            return

        if not user.check_password(password.data):
            raise ValidationError("Invalid password.")

class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "john@doe.com"})
    password = StringField("Password", validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    confirm_password = StringField("Confirm Password", validators=[DataRequired(),
    EqualTo("password", message="Must be identical to password.")], widget=PasswordInput(hide_value=False))
    recaptcha = RecaptchaField()
    submit = SubmitField("Create Account")

    #checks that email is unique
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is registered to another account.")

class ChangeEmailForm(FlaskForm):
    email = StringField("New Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Set New Email")

    def __init__(self, original_email, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        #if there is a change in email, make sure new email is not in database
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError("This email is registered to another account.")
