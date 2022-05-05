from functools import wraps

from flask import flash, redirect, url_for
from decorators.dependency_injection.injector_di import injector
from interfaces.authentication_interface import IAuthentication


def check_if_admin(setup):
    @wraps(setup)
    @injector
    def wrapper(authentication: IAuthentication, *args, **kwargs):
        if not authentication.is_logged_in():
            flash('You need to be an admin to access this feature!')
            return redirect(url_for('main'))
        admin = authentication.get_user_details().admin
        if not admin:
            flash('You need to be an admin to access this feature!')
            return redirect(url_for('post_bp.blog'))
        return setup(*args, **kwargs)
    return wrapper
