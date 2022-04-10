from flask import Blueprint, flash, render_template, request, redirect, url_for
from interfaces.database_upgrade_interface import IDatabaseUpgrade
from interfaces.db_config_interface import IDatabaseConfig
from databases.database_settings import DatabaseSettings
from decorators.dependency_injection.injector_di import injector
database_bp = Blueprint('database_bp', __name__)


@database_bp.route('/setup/', methods=['GET', 'POST'])
@injector
def setup(db_config: IDatabaseConfig, db_upgrade: IDatabaseUpgrade):
    if db_config.is_configured():
        flash("Database already configured")
        return redirect(url_for("main"))
    if request.method == "POST":
        database_settings = DatabaseSettings(
            request.form.get("host"),
            request.form.get("database"),
            request.form.get("user"),
            request.form.get("password"))
        db_config.save(database_settings)
        db_upgrade.upgrade_db()
        flash("Database configured!")
        return redirect(url_for("main"))
    return render_template("db_setup.html")
