from datetime import datetime


class User:
    def __init__(self, name, email, password, admin=False, user_id=0):
        self.id = user_id
        self.name = str(name)
        self.email = str(email)
        self.password = str(password)
        self.created_at = datetime.now().strftime("%B %d %Y %H:%M:%S")
        self.modified_at = ''
        self.admin = admin
