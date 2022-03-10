from interfaces.db_config_interface import IDatabaseConfig
from interfaces.post_repository_interface import IPostRepository
from interfaces.database_interface import IDatabase
from databases.database_config import DatabaseConfig
from databases.database_manager import Database
from databases.memory_database import MemoryDatabase
from databases.memory_database_config import MemoryDatabaseConfig
from repositories.post_db_repo import PostDbRepo
from repositories.post_repo import PostRepo


class ContainerService:
    testing_config :bool
    memory_repo = PostRepo()
    memory_config = MemoryDatabaseConfig()
    services_production = {
    IPostRepository: PostDbRepo(Database(DatabaseConfig())),
    IDatabaseConfig: DatabaseConfig(),
    IDatabase: Database(DatabaseConfig())
    }
    services_memory = {
    IPostRepository: memory_repo,
    IDatabaseConfig: memory_config,
    IDatabase:MemoryDatabase()
    }

    @classmethod
    def get_service(cls):
        if cls.testing_config:
            return cls.services_memory
        return cls.services_production
