from datetime import datetime
import itertools
class Post:
    id = itertools.count()
    def __init__(self, title, contents, owner): 
        self.postId = next(self.id)
        self.postTitle = str(title)
        self.postContents = str(contents)
        self.postOwner = str(owner)
        self.postDateCreation = datetime.now().strftime("%B %d %Y")
        self.postDateModification = ''