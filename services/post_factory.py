from services.post_repo import PostRepo
from services.post_db_repo import PostDbRepo

class PostFactory(object):
    def create(config):
        if config is True:
            return PostRepo()
        else:
            return PostDbRepo()

    create = staticmethod(create)