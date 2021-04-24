from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    data = request.form #the form attribute of our request has all of the data which was sent as part of the form
    if request.method == 'POST':
        print(data)
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return "<p>logout</p>"


@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email)< 4:
            flash('Email must be greater than 4 characters', category="error")
        elif len(fullname) < 2:
            flash('Fullname must be greater than 2 characters', category="error")
        elif password1 != password2:
            flash('Passwords don\'t match', category="error")
        elif len(password1) < 5:
            flash('Passwords must be at least 5 characters', category="error")
        else:
            u = User(email=email, username=fullname, password=password1) #in the secure application we should hash the password with the werkzeug package
            db.session.add(u)
            db.session.commit()
            flash('Account created!', category="success")
            return redirect(url_for('views.home'))
    return render_template("sign_up.html")

@auth.route("/profile")
def profile():
    return render_template("profile.html")