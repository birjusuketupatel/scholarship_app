from app import app
from flask import render_template, url_for, redirect
from app.forms import LoginForm

#home page
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")

#login page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for("index"))

    return render_template("login.html", title="Log In", form=form)
