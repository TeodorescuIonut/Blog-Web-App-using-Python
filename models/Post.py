from datetime import datetime
class Post:
    def __init__(self, title, contents, owner):
        self.post_id = None
        self.post_title = str(title)
        self.post_contents = str(contents)
        self.post_owner = str(owner)
        self.post_date_creation = datetime.now().strftime("%B %d %Y %H:%M:%S")
        self.post_date_modification = ''
