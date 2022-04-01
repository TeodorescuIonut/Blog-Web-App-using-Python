from datetime import datetime
class Post:
    def __init__(self,owner, title, contents, owner_id):
        self.post_id = 0
        self.post_owner = str(owner)
        self.post_title = str(title)
        self.post_contents = str(contents)
        self.post_date_creation = datetime.now().strftime("%B %d %Y %H:%M:%S")
        self.post_date_modification = ''
        self.owner_id = owner_id
