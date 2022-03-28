
from datetime import datetime
from decorators.authorization.check_if_admin_or_owner import check_if_admin_or_owner
from decorators.authorization.check_if_admin import check_if_admin
from decorators.setup.setup import check_setup
from decorators.dependency_injection.injector_di import injector
from flask import Blueprint, flash, g, render_template, request, redirect, session, url_for
from interfaces.authentication_interface import IAuthentication
from interfaces.user_repository_interface import IUserRepository
from interfaces.password_interface import IPassword
from models.user import User


@injector
class UserBlueprint:
    repo:IUserRepository
    password_hash:IPassword
    auth:IAuthentication

    def __init__(self,repo:IUserRepository, password_hash:IPassword, authentication:IAuthentication):   
        self.repo = repo
        self.pass_hash = password_hash
        self.user_bp = Blueprint('user_bp',__name__)
        self.auth = authentication


    def create(self):       
        self.user_bp.route('/')(self.home)
        self.user_bp.route('/USER')(self.home)
        self.user_bp.route('/CREATE/users', methods =["GET", "POST"])(self.add_user)
        self.user_bp.route('/VIEW/<int:user_id>')(self.view_user)
        self.user_bp.route('/UPDATE/<int:user_id>', methods =["GET", "POST"])(self.update_user)
        self.user_bp.route('/DELETE/<int:user_id>', methods =["GET", "POST"])(self.delete_user)
        self.user_bp.context_processor(self.context_processor)
        return self.user_bp
    
    def context_processor(self):
        if self.auth.is_logged_in():
            user= self.auth.get_user_details()
        else:
            user = None
        return dict(logged_user = user,logged_in = self.auth.is_logged_in())
        

    @check_setup
    @check_if_admin
    def home(self):
        return render_template("home.html", users = self.repo.get_all(), length = len(self.repo.users))
    
    @check_setup
    @check_if_admin
    def add_user(self):
        if request.method == "POST":
            user_name = request.form.get("name")
            user_email = request.form.get("email")
            user_password = request.form.get("password")
            admin = bool(request.form.get("make_admin"))
            if admin is not True:
                admin = False
            error = None
            if not user_name:
                error = "Please add a name"
            elif not user_email:
                error = "Please add an email"
            elif not user_password:
                error = "Please add a password"
            if error:
                flash(error)
                user = User(user_name,user_email, user_password, admin)
                return render_template("add_user.html", user = user, urlPage = self.add_user)
            new_user =  User(
                    user_name,
                    user_email,
                    self.pass_hash.generate_password(user_password),admin)
            if self.repo.check_user_email(new_user):
                flash("User email already used")
                return render_template("add_user.html", user = new_user, urlPage = self.add_user)
            self.repo.create(new_user)
            flash("User added")
            return redirect(url_for('user_bp.view_user', user_id = new_user.user_id))
        return render_template("add_user.html", user = User, urlPage = self.add_user)

    @check_setup
    def view_user(self,user_id):
            user = self.repo.get_by_id(user_id)
            if not user:
                flash("User not found")
                return render_template("home.html")
            return render_template("view_user.html", user = user)

    @check_setup
    @check_if_admin_or_owner
    def update_user(self,user_id):
        user:User = self.repo.get_by_id(user_id)
        if request.method == "POST":
            user_name = request.form.get("name")
            user_email = request.form.get("email")
            user_password = request.form.get("password")
            make_user = bool(request.form.get("make_user"))
            admin = bool(request.form.get("make_admin"))
            if admin is None:
                admin = user.admin
            if make_user is True:
                admin = False
            if user_password =="":
                user_password = user.user_password
            else:
                user_password = self.pass_hash.generate_password(user_password)
            if not user_name :
                user_name = user.user_name
            elif not user_email:
                user_email =  user.user_email
            user.user_id = user_id
            user.user_name = user_name
            user.user_email = user_email
            user.user_password = user_password
            user.user_date_modification = datetime.now().strftime("%B %d %Y")
            user.admin = admin
            self.repo.update(user)
            flash("User updated")
            return redirect(url_for('user_bp.view_user',user_id = user.user_id))
        return render_template("add_user.html",
                user = user, buttonText = "Update",
                urlPage = self.update_user)
    
    @check_setup
    @check_if_admin
    def delete_user(self,user_id):
        user = self.repo.get_by_id(user_id)
        self.repo.delete(user)
        flash("User deleted")
        return redirect(url_for('user_bp.home'))