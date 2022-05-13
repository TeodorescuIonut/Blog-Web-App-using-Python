from models.dtos.user import User
from interfaces.user_repository_interface import IUserRepository
from services.password_hash import generate_password_hash


class UserRepo(IUserRepository):
    users = list()
    count = 0
    users.append(User("admin", "admin@localhost.com", generate_password_hash("1234"), True, 999))

    def get_all(self) -> []:
        sorted_array = sorted(self.users, key=lambda x: x.created_at, reverse=True)
        return sorted_array

    def get_by_id(self, user_id: int) -> User:
        for user in self.users:
            if user.id == user_id:
                return user

    def check_user_email(self, user_to_check: User) -> bool:
        if len(self.users) > 0:
            for user in self.users:
                if user_to_check.email == user.email:
                    return True

    def create(self, user: User):
        user.id = self.count
        self.users.append(user)
        self.count += 1

    def update(self, user: User) -> None:
        self.users.remove(user)
        self.users.append(user)

    def delete(self, user: User) -> None:
        self.users.remove(user)

    def get_user_by_email(self, user_email):
        for user in self.users:
            if user.email == user_email:
                return user
