from app import app, login_manager, db
from flask import render_template, url_for, redirect, request, flash
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.token import generate_confirmation_token, check_token
from flask_login import current_user, login_user, logout_user, login_required
from wtforms import StringField, BooleanField, SubmitField
from app.email import send_email

#home page
@app.route("/")
@app.route("/index")
@login_required
def index():
    if not current_user.is_confirmed:
        flash("Your email is not confirmed.")

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

        #generates verification token for user's email
        #emails url to user
        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for("confirm", token=token, _external=True)
        body = render_template("confirmation_email.html", confirm_url=confirm_url)
        subject = "Confirm Your Email"
        send_email(new_user.email, subject, body)

        return redirect(url_for("login"))

    #builds form based on custom template for each field
    field_to_template = {"StringField": "_stringfield.html",
                       "SubmitField": "_submitfield.html",
                       "RecaptchaField": "_recaptchafield.html"}
    field_to_error = {"StringField": "_fielderror.html"}

    components = render_fields(form, field_to_template, field_to_error)

    return render_template("register.html", title="New Account", form=form, components=components)

#profile page
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html", title=current_user.first_name)

#resends confirmation email
@app.route("/resend", methods=["GET", "POST"])
@login_required
def resend():
    #generates new verification token
    #resends verification email
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for("confirm", token=token, _external=True)
    body = render_template("confirmation_email.html", confirm_url=confirm_url)
    subject = "Confirm Your Email"
    send_email(current_user.email, subject, body)

    flash("New confirmation email sent.")

    return redirect(url_for("profile"))

#log out page
@app.route("/logout", methods=["GET", "POST"])
def logout():
    #logs out user
    #instantly redirects them to login page
    logout_user()
    return redirect(url_for("login"))

#email confirmation page
@app.route("/confirm/<token>", methods=["GET", "POST"])
@login_required
def confirm(token):
    email = check_token(token)

    if not email:
        flash("Confirmation link is invalid or expired.")
        return redirect(url_for("index"))

    user = User.query.filter_by(email=email).first_or_404()

    if user.is_confirmed:
        flash("Email is already confirmed.")
    else:
        user.is_confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("Email has been confirmed.")

    return redirect(url_for("index"))

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
