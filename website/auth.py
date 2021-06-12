from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            correctPWD = check_password_hash(user.password, password)
            if correctPWD:
                login_user(user)
                flash("<strong>Success:</strong> Login Success!", "success")
                return redirect("/")
        flash("<strong>Error:</strong> Email or Password is Incorrect", category="danger")
    return render_template("Login.html", L="active")


@auth.route('/logout')
def logout():
    logout_user()
    flash("<strong>Success:</strong> Logout Success!", "success")
    return redirect("/login")


@auth.route("/signUp", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user_exists = User.query.filter_by(email=email).first()
        if len(email) < 4:
            flash("<strong>Error:</strong> Email is Too Short (Must be more than 4 Chars )", category='danger')
        elif len(first_name) < 2:
            flash("<strong>Error:</strong> First Name is Too Short (Must be more than 1 Char )", category='danger')
        elif len(last_name) < 2:
            flash("<strong>Error:</strong> Last Name is Too Short (Must be more than 1 Char )", category='danger')
        elif len(password1) < 8:
            flash("<strong>Error:</strong> Password is Too Short (Must be more than 7 Chars )", category='danger')
        elif password1 != password2:
            flash("<strong>Error:</strong> Both Passwords Don't Match", category='danger')
        elif user_exists:
            flash("<strong>Error:</strong> That Email Already Exists!", category='danger')
        else:
            new_user = User(email=email, name=f"{first_name} {last_name}", password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("<strong>Success:</strong> Account Created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", S="active")


