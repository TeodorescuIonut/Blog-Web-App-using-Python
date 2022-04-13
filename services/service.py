from interfaces.image_support_interface import IImageRepo
from interfaces.database_upgrade_interface import IDatabaseUpgrade
from interfaces.databse_sqlalchemy_interface import IDatabaseAlchemy
from interfaces.db_config_interface import IDatabaseConfig
from interfaces.filtering_interface import IFiltering
from interfaces.pagination_interface import IPagination
from interfaces.post_repository_interface import IPostRepository
from interfaces.database_interface import IDatabase
from interfaces.user_repository_interface import IUserRepository
from interfaces.password_interface import IPassword
from interfaces.authentication_interface import IAuthentication
from databases.database_upgrade_memory import MemoryDBUpgrade
from databases.sql_alchemy_database_manager import SQLAlchemyDatabase
from databases.database_config import DatabaseConfig
from databases.database_manager import Database
from databases.memory_database import MemoryDatabase
from databases.memory_database_config import MemoryDatabaseConfig
from repositories.post_db_repo import PostDbRepo
from repositories.post_repo import PostRepo
from repositories.sql_alchemy_post_repo import SQLAlchemyPostRepo
from repositories.sql_alchemy_user_repo import SQLAlchemyUserRepo
from repositories.user_db_repo import UserDbRepo
from repositories.user_repo import UserRepo
from services.filtering import Filtering
from services.paginate import Paginate
from services.password_hash import PasswordHashing
from services.authentication import Authentication
from services.database_upgrade_create import DatabaseUpgradeAndCreate
from services.image_repo import ImageRepo


class ContainerService:
    testing_config: bool
    memory_post_repo = PostRepo()
    memory_user_repo = UserRepo()
    memory_config = MemoryDatabaseConfig()
    memory_upgrade = MemoryDBUpgrade()

    services_production = {
        IPostRepository: PostDbRepo(Database(DatabaseConfig()), ImageRepo()),
        IUserRepository: UserDbRepo(Database(DatabaseConfig())),
        IDatabaseConfig: DatabaseConfig(),
        IDatabase: Database(DatabaseConfig()),
        IPassword: PasswordHashing(),
        IAuthentication: Authentication(UserDbRepo(Database(DatabaseConfig())), PasswordHashing()),
        IDatabaseUpgrade: DatabaseUpgradeAndCreate(Database(DatabaseConfig()), DatabaseConfig()),
        IPagination: Paginate(),
        IFiltering: Filtering(UserDbRepo(Database(DatabaseConfig()))),
        IImageRepo: ImageRepo()
    }
    services_memory = {
        IPostRepository: memory_post_repo,
        IUserRepository: memory_user_repo,
        IDatabaseConfig: memory_config,
        IDatabase: MemoryDatabase(),
        IPassword: PasswordHashing(),
        IAuthentication: Authentication(memory_user_repo, PasswordHashing()),
        IDatabaseUpgrade: memory_upgrade,
        IPagination: Paginate(),
        IFiltering: Filtering(memory_user_repo)
    }

    services_sqlalchemy = {
        IPostRepository: SQLAlchemyPostRepo(SQLAlchemyDatabase(DatabaseConfig()), ImageRepo()),
        IUserRepository: SQLAlchemyUserRepo(SQLAlchemyDatabase(DatabaseConfig())),
        IDatabaseConfig: DatabaseConfig(),
        IDatabaseAlchemy: SQLAlchemyDatabase(DatabaseConfig()),
        IPassword: PasswordHashing(),
        IAuthentication: Authentication(SQLAlchemyUserRepo(
            SQLAlchemyDatabase(DatabaseConfig())),
            PasswordHashing()),
        IDatabaseUpgrade: DatabaseUpgradeAndCreate(
            Database(DatabaseConfig()),
            DatabaseConfig()),
        IPagination: Paginate(),
        IFiltering: Filtering(SQLAlchemyUserRepo(SQLAlchemyDatabase(DatabaseConfig()))),
        IImageRepo: ImageRepo()
    }

    @classmethod
    def get_service(cls):
        if cls.testing_config:
            return cls.services_memory
        # return cls.services_production
        return cls.services_sqlalchemy
