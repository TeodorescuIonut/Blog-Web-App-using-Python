import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
from services.post_repository_interface import IPostRepository
from models.post_preview import PostPreview



class PostRepo(IPostRepository):
    def __init__(self):
        self.posts = list()
        self.count = 0

    def get_all(self):
        sorted_array = sorted(self.get_previews(),key=lambda x: x.post_date_creation,reverse=True)
        return sorted_array

    def get_by_id(self, post_id):
        for post in self.posts:
            if post.post_id == post_id:
                return post
    def create(self, post):
        post.post_id = self.count
        self.posts.append(post)
        self.count += 1
    def update(self, post):
        self.posts.remove(post)
        self.posts.append(post)

    def delete(self, post):
        self.posts.remove(post)
    
    def get_previews(self):
        posts_previews = []
        for post in self.posts:
            posts_previews.append(self.create_preview(post))
        return posts_previews

    def create_preview(self,post):
        content_preview = post.post_contents[0:200]
        creation_date = post.post_date_creation
        modification_date = post.post_date_modification
        preview = PostPreview(post.post_id,post.post_title, content_preview, post.post_owner, creation_date, modification_date)
        return preview

