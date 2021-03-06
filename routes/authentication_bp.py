from flask import Blueprint, flash, redirect, render_template, request, url_for
from decorators.dependency_injection.injector_di import injector
from decorators.setup.setup import check_setup
from interfaces.authentication_interface import IAuthentication
from models.dtos.user import User

authenticate = Blueprint('authenticate', __name__)


@authenticate.route('/SIGNIN/', methods=["GET", "POST"])
@injector
@check_setup
def sign_in(authentication: IAuthentication):
    status = authentication.is_logged_in()
    if authentication.is_logged_in():
        flash('You are already logged in.')
        return redirect(url_for('post_bp.blog'))
    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        if authentication.sign_in(user_email, user_password):
            user: User = authentication.get_user_details()
            flash(f"Welcome back {user.name}")
            return redirect(url_for('post_bp.blog'))
        else:
            flash("Wrong password or user, please try again.")
            return render_template("sign-in.html", user_email=user_email)
    return render_template("sign-in.html", logged_in=status, user=User)


@authenticate.route('/SIGNOUT/', methods=["GET", "POST"])
@injector
@check_setup
def sign_out(authentication: IAuthentication):
    if authentication.sign_out():
        flash('You have been logged out')
        return redirect(url_for("post_bp.blog"))
    return render_template("sign-in.html")
