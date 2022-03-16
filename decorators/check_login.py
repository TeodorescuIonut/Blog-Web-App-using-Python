
from functools import wraps
from flask import flash, redirect, session, url_for
from decorators.injector_di import injector
from interfaces.authentication_interface import IAuthentication


def check_login(setup): 
    @wraps(setup)
    @injector
    def wrapper(authentication:IAuthentication,*args, **kwargs):
        if authentication.is_logged_in():
            return setup(authentication.is_logged_in(),*args, **kwargs)
    return wrapper