from functools import wraps
from databases.database_config import DatabaseConfig
from flask import redirect, request, url_for


def check_setup(setup):
    @wraps(setup)
    def wrapper():
        if DatabaseConfig().is_configured() is False and request.endpoint != "database_bp.setup":
            return redirect(url_for('database_bp.setup'))

    return wrapper