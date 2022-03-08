from functools import wraps
from databases.database_config import DatabaseConfig
from flask import redirect, render_template, request, url_for
from services.services import Services
from interfaces.post_repository_interface import IPostRepository


def check_setup(setup):
    @wraps(setup)
    def wrapper(*args, **kwargs):
        if DatabaseConfig().is_configured() is False and request.endpoint != "database_bp.setup":
            return redirect(url_for('database_bp.setup'))
        return setup(*args, **kwargs)
    return wrapper

def injector(func):
    @wraps(func)
    def wrapper_services(*args, **kwargs):
        service = Services.get_service()
        value = func(service, *args, **kwargs)
        return value
    return wrapper_services