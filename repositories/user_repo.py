from flask import Response

from models.user import User
from interfaces.user_repository_interface import IUserRepository
from services.password_hash import generate_password_hash


class UserRepo(IUserRepository):
    users = list()
    count = 0
    users.append(User("admin", "admin@localhost.com", generate_password_hash("1234"), True, 999))

    def get_all(self) -> list():
        sorted_array = sorted(self.users, key=lambda x: x.user_date_creation, reverse=True)
        return sorted_array

    def get_by_id(self, user_id: int) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user

    def check_user_email(self, user_to_check: User) -> bool:
        if len(self.users) > 0:
            for user in self.users:
                if user_to_check.user_email == user.user_email:
                    return True

    def create(self, user: User) -> (Response | str):
        user.user_id = self.count
        self.users.append(user)
        self.count += 1

    def update(self, user: User) -> None:
        self.users.remove(user)
        self.users.append(user)

    def delete(self, user: User) -> None:
        self.users.remove(user)

    def get_user_by_email(self, user_email):
        for user in self.users:
            if user.user_email == user_email:
                return user
