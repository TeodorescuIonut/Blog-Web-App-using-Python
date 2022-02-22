
from flask import Blueprint, flash, render_template, request, redirect, url_for
from databases.database_manager import Database

database_bp = Blueprint('database_bp', __name__)

@database_bp.route('/DB_SETUP/', methods = ['GET', 'POST'])
def db_setup():
    if Database.configured is True:
        flash("Database already configured")
        return redirect(url_for("app.main"))
    if request.method == "POST":    
        host = request.form.get("host")
        database = request.form.get("database")
        user = request.form.get("user")
        password = request.form.get("password")
        db = Database()
        db.get_con_details(host, database, user, password)
        db.configured = True
        flash("Database configured!")
        return redirect(url_for("app.main"))
    return render_template("db_setup.html")