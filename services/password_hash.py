from werkzeug.security import generate_password_hash, check_password_hash
from interfaces.password_interface import IPassword


class PasswordHashing(IPassword):
    def generate_password(self, password):
        return generate_password_hash(password, "sha256")

    def check_password(self, hash_password, password):
        return check_password_hash(hash_password, password)
