from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Logged in successfully', category='success')
                login_user(user, remember=True) #remember that the user is logged in, stored in the flask session data, unless webserver restarts or user clears its browser history, he is remembered
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category="error")
        elif len(email)< 4:
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
            login_user(user, remember=True) #remember that the user is logged in, stored in the flask session data, unless webserver restarts or user clears its browser history, he is remembered
            flash('Account created!', category="success")
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)

@auth.route("/logout")
@login_required #using this decorator, we cannot access this page unless the user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/profile")
def profile():
    return render_template("profile.html")