from functools import wraps

from flask import flash, redirect, url_for

from decorators.injector_di import injector
from interfaces.authentication_interface import IAuthentication


def check_if_admin(setup): 
    @wraps(setup)
    @injector
    def wrapper(authentication: IAuthentication,*args, **kwargs):
        if authentication.is_admin() is False:
            flash('You need to be an administrator to access this feature!')
            return redirect(url_for('main'))
        return setup(*args, **kwargs)
    return wrapper