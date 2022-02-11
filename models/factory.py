import sys
import os

from pathlib import Path
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
from PostsRepo.post_repo import PostRepo
from PostsRepo.post_db_repo import PostDbRepo

class Repo(object):
    def factory(type):
        if type == "PostRepo":
            return PostRepo()
        if type == "PostDbRepo":
            return PostDbRepo()

    factory = staticmethod(factory)