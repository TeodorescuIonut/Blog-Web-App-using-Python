from unittest.mock import Mock
from databases.database_config import DatabaseConfig
from interfaces.db_config_interface import IDatabaseConfig
from services.post_db_repo import PostDbRepo
from services.post_repo import PostRepo
from interfaces.post_repository_interface import IPostRepository


class Services:
    testing_config :bool
    services_memory = {
    IPostRepository: PostRepo(),
    IDatabaseConfig: Mock()  
    }
    services_production = {
    IPostRepository: PostDbRepo(),
    IDatabaseConfig: DatabaseConfig()
    }
    @classmethod
    def get_service(cls):
        if cls.testing_config:
            return cls.services_memory[IPostRepository]
        return cls.services_production[IPostRepository]
