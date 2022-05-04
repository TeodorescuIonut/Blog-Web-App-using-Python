from functools import wraps

from flask import flash, redirect, url_for

from decorators.dependency_injection.injector_di import injector
from interfaces.authentication_interface import IAuthentication


def check_if_admin_or_owner(setup):
    @wraps(setup)
    @injector
    def wrapper(authentication: IAuthentication, *args, **kwargs):
        if authentication.is_logged_in() is True:
            user_id = kwargs["user_id"]
            singed_user_id = authentication.get_user_details().id
            admin = authentication.get_user_details().admin
            if user_id != singed_user_id and admin is False:
                flash("403 - Not allowed")
                return redirect(url_for('main'))
        else:
            flash("403 - Not allowed")
            return redirect(url_for('main'))
        return setup(*args, **kwargs)

    return wrapper
