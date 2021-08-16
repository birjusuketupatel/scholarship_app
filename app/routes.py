from app import app, login_manager
from flask import render_template, url_for, redirect, request
from werkzeug.urls import url_parse
from app.forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required

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

    return render_template("login.html", title="Log In", form=form)

#log out page
@app.route("/logout", methods=["GET", "POST"])
def logout():
    #logs out user
    #instantly redirects them to login page
    logout_user()
    return redirect(url_for("login"))
