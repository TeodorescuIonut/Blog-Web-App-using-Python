
from functools import wraps
from flask import flash, redirect, session, url_for


def check_login(setup): 
    @wraps(setup)
    def wrapper(*args, **kwargs):
        if "id" in session:
            flash('You are already logged in.')
            return redirect(url_for('main'))
        return setup(*args, **kwargs)
    return wrapper