from functools import wraps
from flask import flash, redirect, url_for
from decorators.dependency_injection.injector_di import injector
from interfaces.authentication_interface import IAuthentication
from interfaces.post_repository_interface import IPostRepository



def check_if_post_owner_or_admin(setup):
    @wraps(setup)
    @injector
    def wrapper(repo: IPostRepository,authentication:IAuthentication, *args, **kwargs):
        post_id= kwargs["post_id"]
        user_id = 0
        signed_user_id = None
        admin = False
        if isinstance(repo,IPostRepository):
            user_id = repo.get_by_id(post_id).owner_id
        if isinstance(authentication, IAuthentication):
            signed_user_id = authentication.get_user_details().user_id
            admin = authentication.get_user_details().admin
        if  user_id  != signed_user_id and admin is False:
            flash("403 - Not allowed")
            return redirect(url_for('main'))
        return setup(*args, **kwargs)
    return wrapper
