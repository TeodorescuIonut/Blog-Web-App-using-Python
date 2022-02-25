from configparser import ConfigParser
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

database_bp = Blueprint('database_bp', __name__)


@database_bp.route('/setup', methods = ['GET', 'POST'])
def setup():
    if DatabaseConfig().is_configured() is True:
        flash("Database already configured")
        return redirect(url_for("post_bp.blog"))
    else:
        if request.method == "POST":         
            host = request.form.get("host")
            database = request.form.get("database")
            user = request.form.get("user")
            password = request.form.get("password")
            config_db = DatabaseConfig() 
            config_db.save(host, database, user,password)
            Database().create_table()
            flash("Database configured!")
            return redirect(url_for("post_bp.blog"))
        return render_template("db_setup.html")