import sys
import os
from pathlib import Path
from PostsRepo.post_repository_interface import IPostRepository
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)


class PostDbRepo(IPostRepository):
    def create(self, post):
        return super().create(post)
    def get_all(self):
        return super().get_all()
    def get_by_id(self, post_id):
        return super().get_by_id(post_id)
    def update(self, post):
        return super().update(post)
    def delete(self, post):
        return super().delete(post)
    def get_previews(self):
        return super().get_previews()
    def create_preview(self, post):
        return super().create_preview(post)
        