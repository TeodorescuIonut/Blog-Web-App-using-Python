from services.post_repo import PostRepo
from services.post_db_repo import PostDbRepo



class PostFactory(object):
    def create(repo):
        if repo == "PostRepo":
            return PostRepo()
        if repo == "PostDbRepo":
            return PostDbRepo()

    create = staticmethod(create)