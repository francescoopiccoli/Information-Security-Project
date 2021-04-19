from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return "<p>logout</p>"


@auth.route("/sign-up")
def signup():
    return render_template("sign_up.html")

@auth.route("/profile")
def profile():
    return render_template("profile.html")