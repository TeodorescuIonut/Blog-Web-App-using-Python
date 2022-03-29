from flask import session
from interfaces.authentication_interface import IAuthentication
from interfaces.user_repository_interface import IUserRepository
from interfaces.password_interface import IPassword
from models.user import User


class Authentication(IAuthentication):
    repo:IUserRepository
    password_hash:IPassword
    user:User
    email:str = ""
    def __init__(self, repo:IUserRepository, password_hash:IPassword):
        self.repo = repo
        self.password_hash = password_hash

    def sign_in(self, user_email, password)-> bool:
        self.user:User = self.repo.get_user_by_email(user_email)
        if self.user is not None and self.password_hash.check_password(self.user.user_password,
        password):
            session['user_id'] = self.user.user_id
            session['user_name'] = self.user.user_name
            if self.user.admin is True:
                session['admin'] = "true"
            else:
                session['admin'] = "false"
            self.email = user_email
            return True
        return False

    def sign_out(self) -> bool:
        if 'user_id' in session:
            session.pop("user_id", None)
            session.pop("user_name",None)
            session.pop("admin", None)
            return True
        return False

    def get_user_details(self)-> User:
        return self.repo.get_user_by_email(self.email)

    def is_logged_in(self) -> bool:
        if "user_id" in session:
            return True
