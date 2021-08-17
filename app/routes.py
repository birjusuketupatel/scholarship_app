from app import app, login_manager, db
from flask import render_template, url_for, redirect, request
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from wtforms import StringField, BooleanField, SubmitField
from app import mail
from flask_mail import Message

#home page
@app.route("/")
@app.route("/index")
@login_required
def index():

    return render_template("index.html", title="Home")

#log in page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    #on valid submission, logs in and redirects to next
    if form.validate_on_submit():
        #logs in user
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember_me.data)

        #if next is invalid, redirects to home
        #else redirects to next
        next_page = request.args.get("next")
        if next_page is None or url_parse(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)

    #builds form based on custom template for each field
    field_to_template = {"StringField": "_stringfield.html",
                       "BooleanField": "_booleanfield.html",
                       "SubmitField": "_submitfield.html"}
    field_to_error = {"StringField": "_fielderror.html"}

    components = render_fields(form, field_to_template, field_to_error)

    return render_template("login.html", title="Log In", form=form, components=components)

#register new account page
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        #adds new user to database
        #redirects to login
        new_user = User(email=form.email.data, first_name=form.first_name.data,
                        last_name=form.last_name.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    #builds form based on custom template for each field
    field_to_template = {"StringField": "_stringfield.html",
                       "SubmitField": "_submitfield.html",
                       "RecaptchaField": "_recaptchafield.html"}
    field_to_error = {"StringField": "_fielderror.html"}

    components = render_fields(form, field_to_template, field_to_error)

    return render_template("register.html", title="New Account", form = form, components=components)

#log out page
@app.route("/logout", methods=["GET", "POST"])
def logout():
    #logs out user
    #instantly redirects them to login page
    logout_user()
    return redirect(url_for("login"))

#given a form, map of field type to field template,
#and map of field type to error template
#returns a list of rendered html
def render_fields(form, field_to_template, field_to_error):
    components = []
    for field in form:
        field_type = type(field).__name__

        if field_type in field_to_template:
            template_name = field_to_template[field_type]
            components.append(render_template(template_name, field=field))

        if field_type in field_to_error:

            error_template = field_to_error[field_type]
            components.append(render_template(error_template, field=field))

    return components
