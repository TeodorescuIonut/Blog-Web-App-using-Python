from interfaces.db_config_interface import IDatabaseConfig
from interfaces.post_repository_interface import IPostRepository
from interfaces.database_interface import IDatabase
from databases.database_config import DatabaseConfig
from databases.database_manager import Database
from databases.memory_database import MemoryDatabase
from databases.memory_database_config import MemoryDatabaseConfig
from interfaces.user_repository_interface import IUserRepository
from interfaces.password_interface import IPassword
from repositories.post_db_repo import PostDbRepo
from repositories.post_repo import PostRepo
from repositories.user_db_repo import UserDbRepo
from repositories.user_repo import UserRepo
from services.password_hash import PasswordHashing


class ContainerService:
    testing_config :bool
    memory_post_repo = PostRepo()
    memory_user_repo = UserRepo()       
    memory_config = MemoryDatabaseConfig()
    services_production = {
    IPostRepository: PostDbRepo(Database(DatabaseConfig())),
    IUserRepository: UserDbRepo(Database(DatabaseConfig())),
    IDatabaseConfig: DatabaseConfig(),
    IDatabase: Database(DatabaseConfig()),
    IPassword: PasswordHashing()
    }
    services_memory = {
    IPostRepository: memory_post_repo,
    IUserRepository: memory_user_repo,
    IDatabaseConfig: memory_config,
    IDatabase:MemoryDatabase(),
    IPassword: PasswordHashing()
    }

    @classmethod
    def get_service(cls):
        if cls.testing_config:
            return cls.services_memory
        return cls.services_production
