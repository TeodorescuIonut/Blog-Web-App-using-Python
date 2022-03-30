from functools import wraps

from flask import flash, redirect, url_for
from decorators.dependency_injection.injector_di import injector
from interfaces.post_repository_interface import IPostRepository



def check_post_exists(setup):
    @wraps(setup)
    @injector
    def wrapper(repo:IPostRepository,*args, **kwargs):
        post_id = kwargs['post_id']
        if repo.get_by_id(post_id) is None:
            flash("Post doesn't exists!")
            return redirect(url_for('main'))
        return setup(*args, **kwargs)
    return wrapper