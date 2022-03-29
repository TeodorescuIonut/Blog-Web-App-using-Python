
from functools import wraps
from flask import flash, redirect, url_for
from decorators.dependency_injection.injector_di import injector
from interfaces.authentication_interface import IAuthentication


def sign_in_required(setup):
    @wraps(setup)
    @injector
    def wrapper(authentication: IAuthentication,*args, **kwargs):
        if authentication.is_logged_in() is not True:
            flash('You need to sign in to access this feature!')
            return redirect(url_for('main'))
        return setup(*args, **kwargs)
    return wrapper
