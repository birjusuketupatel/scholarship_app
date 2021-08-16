from app import app, login_manager
from flask import render_template, url_for, redirect
from app.forms import LoginForm
from app.models import User
from flask_login import login_user

#home page
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")

#login page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    #on valid submission, logs in user and redirect to home
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))

    return render_template("login.html", title="Log In", form=form)
