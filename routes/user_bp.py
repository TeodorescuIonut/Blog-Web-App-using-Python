from datetime import datetime
from decorators.setup import check_setup
from decorators.injector_di import injector
from flask import Blueprint, flash, render_template, request, redirect, url_for
from interfaces.user_repository_interface import IUserRepository
from interfaces.password_interface import IPassword
from models.user import User


@injector
class UserBlueprint:
    repo:IUserRepository
    password_hash:IPassword
    def __init__(self,repo:IUserRepository, password_hash:IPassword):   
        self.repo = repo
        self.pass_hash = password_hash
        self.user_bp = Blueprint('user_bp',__name__)

    def create(self):       
        self.user_bp.route('/')(self.home)
        self.user_bp.route('/USER')(self.home)
        self.user_bp.route('/CREATE/users', methods =["GET", "POST"])(self.add_user)
        self.user_bp.route('/VIEW/<int:user_id>')(self.view_user)
        self.user_bp.route('/UPDATE/<int:user_id>', methods =["GET", "POST"])(self.update_user)
        self.user_bp.route('/DELETE/<int:user_id>', methods =["GET", "POST"])(self.delete_user)
        return self.user_bp
   
    @check_setup
    def home(self):
        return render_template("home.html", users = self.repo.get_all(), length = len(self.repo.users))
    @check_setup
    def add_user(self):
        if request.method == "POST":
            user_name = request.form.get("name")
            user_email = request.form.get("email")
            user_password = request.form.get("password")
            user = User(user_name , user_email, self.pass_hash.generate_password(user_password))
            error = None
            if not user_name:
                error = "Please add a name"
            elif not user_email:
                error = "Please add an email"
            elif not user_password:
                error = "Please add password"
            if error:
                flash(error)
                return render_template("add_user.html", user = user, urlPage = self.add_user)
            else:
                new_user =  User(
                    user_name.title(),
                    user_email,
                    user_password)
            self.repo.create(new_user)
            flash("User added")
            return redirect(url_for('user_bp.view_user',user_id = new_user.user_id))
        return render_template("add_user.html", user = User, urlPage = self.add_user)

    @check_setup
    def view_user(self,user_id):
            user = self.repo.get_by_id(user_id)
            return render_template("view_user.html", user = user)

    @check_setup
    def update_user(self,user_id):
        user = self.repo.get_by_id(user_id)
        if request.method == "POST":
            user_name = request.form.get("name")
            user_email = request.form.get("email")
            user_password = request.form.get("password")
            error = None
            if not user_name :
                error = "Please add a name"
            elif not user_email:
                error = "Please add an email"
            if error:
                    flash(error)
                    return render_template("add_user.html",
                    user = user, buttonText = "Update",
                    urlPage = staticmethod(self.update_user))
            else:
                user.user_id = user_id
                user.user_name = user_name
                user.user_email = user_email
                user.user_password = user_password
                user.user_date_modification = datetime.now().strftime("%B %d %Y")
                self.repo.update(user)
                flash("User updated")
            return redirect(url_for('user_bp.view_user',user_id = user.user_id))
        return render_template("add_user.html",
                user = user, buttonText = "Update",
                urlPage = self.update_user)
    @check_setup
    def delete_user(self,user_id):
        user = self.repo.get_by_id(user_id)
        self.repo.delete(user)
        flash("User deleted")
        return redirect(url_for('user_bp.home'))