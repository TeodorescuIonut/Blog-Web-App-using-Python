from decorators.check_login import check_login
from decorators.injector_di import injector
from decorators.setup import check_setup
from flask import Blueprint, flash, redirect, render_template, request, url_for
from interfaces.authentication_interface import IAuthentication
from models.user import User

authenticate = Blueprint('authenticate', __name__)

@authenticate.route('/SIGNIN/', methods = ["GET", "POST"])
@check_login
@injector
@check_setup
def sign_in(authentication: IAuthentication):
    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        if authentication.sign_in(user_email, user_password):
            user:User = authentication.get_user_details(user_email)
            flash(f"Welcome back {user.user_name}")
            return redirect(url_for("main"))
        else:
            flash("Wrong password or user, please try again.")
            return render_template("sign-in.html", email = user_email)
    return render_template("sign-in.html")

@authenticate.route('/SIGNOUT/', methods = ["GET", "POST"])
@injector
@check_setup
def sign_out(authentication: IAuthentication):
    if authentication.sign_out():
        flash('You have been logged out')
        return redirect(url_for("main"))