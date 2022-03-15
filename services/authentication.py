
from flask import session
from interfaces.authentication_interface import IAuthentication
from interfaces.user_repository_interface import IUserRepository
from interfaces.password_interface import IPassword
from models.user import User


class Authentication(IAuthentication):
    repo:IUserRepository
    password_hash:IPassword
    user:User
    def __init__(self, repo:IUserRepository, password_hash:IPassword):
        self.repo = repo
        self.password_hash = password_hash

    def sign_in(self, user_email, password):
        self.user = self.repo.get_user_by_email(user_email)
        if self.user is not None and self.password_hash.check_password(self.user.user_password, password):
            session['id'] = self.user.user_id
            session['user_name'] = self.user.user_name
            return True
        return False

    def sign_out(self):
        session.clear()
        return True

    def get_user_details(self, user_email)-> User:
        return self.repo.get_user_by_email(user_email)


    

    
        
