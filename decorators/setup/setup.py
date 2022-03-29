from functools import wraps
from flask import redirect, request, url_for
from decorators.dependency_injection.injector_di import injector
from interfaces.db_config_interface import IDatabaseConfig



def check_setup(setup):
    @wraps(setup)
    @injector
    def wrapper(config:IDatabaseConfig,*args, **kwargs):
        if config.is_configured() is False and request.endpoint != "database_bp.setup":
            return redirect(url_for('database_bp.setup'))
        return setup(*args, **kwargs)
    return wrapper
