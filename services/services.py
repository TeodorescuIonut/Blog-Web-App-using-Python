
from services.container import Container
from services.post_repository_interface import IPostRepository


class Services(object):
    def __init__(self, config):
        self.config = config
    

    def get_service(self):
        if self.config is True:
            return Container.services_memory[IPostRepository]
        return Container.services_production[IPostRepository]
