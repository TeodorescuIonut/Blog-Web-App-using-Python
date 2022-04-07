from datetime import datetime

class User:
    def __init__(self, name, email, password, admin = False, user_id = 0):
        self.user_id = user_id
        self.user_name = str(name)
        self.user_email = str(email)
        self.user_password = str(password)
        self.user_date_creation = datetime.now().strftime("%B %d %Y %H:%M:%S")
        self.user_date_modification = ''
        self.admin = admin
        