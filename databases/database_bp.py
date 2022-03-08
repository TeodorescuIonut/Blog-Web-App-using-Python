import sys
import os
from pathlib import Path


myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from flask import Blueprint, flash, render_template, request, redirect, url_for
from databases.database_manager import Database
from databases.database_config import DatabaseConfig
from databases.database_settings import DatabaseSettings

database_bp = Blueprint('database_bp', __name__)


@database_bp.route('/setup/', methods = ['GET', 'POST'])
def setup():
    if DatabaseConfig().is_configured():
        flash("Database already configured")
        return redirect(url_for("main"))
    if request.method == "POST":
        database_settings = DatabaseSettings(         
        request.form.get("host"),
        request.form.get("database"),
        request.form.get("user"),
        request.form.get("password"))
        my_config= DatabaseConfig()
        my_config.save(database_settings)
        Database().create_table()
        flash("Database configured!")
        return redirect(url_for("main"))
    return render_template("db_setup.html")