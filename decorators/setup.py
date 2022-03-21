from functools import wraps
from databases.database_config import DatabaseConfig
from decorators.injector_di import injector
from flask import redirect, request, url_for
from interfaces.database_upgrade_interface import IDatabaseUpgrade
from interfaces.db_config_interface import IDatabaseConfig



def check_setup(setup): 
    @wraps(setup)
    @injector
    def wrapper(config:IDatabaseConfig,db_upgrade: IDatabaseUpgrade,*args, **kwargs):
        if config.is_configured() is False and request.endpoint != "database_bp.setup":
            return redirect(url_for('database_bp.setup'))
        db_upgrade.upgrade_db()
        return setup(*args, **kwargs)
    return wrapper

