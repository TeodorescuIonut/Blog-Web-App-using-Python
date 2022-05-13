from datetime import datetime


class Post:
    def __init__(self, owner, title, contents, owner_id, image=None, post_id=0):
        self.id = post_id
        self.owner = str(owner)
        self.title = str(title)
        self.contents = str(contents)
        self.created_at = datetime.now().strftime("%B %d %Y %H:%M:%S")
        self.modified_at = ''
        self.owner_id = owner_id
        self.image = image
