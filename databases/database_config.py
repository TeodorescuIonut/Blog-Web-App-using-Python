from configparser import ConfigParser
import sys
import os
from pathlib import Path

from interfaces.db_config_interface import IDatabaseConfig

myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a = str(path.parent.absolute())
sys.path.append(a)
from databases.database_settings import DatabaseSettings
from databases.config import Config


class DatabaseConfig(IDatabaseConfig, Config):
    def __init__(self) -> None:
        Config.__init__(self)
        self.config = ConfigParser()

    def save(self, database_settings: DatabaseSettings):
        self.config.add_section("postgresql")
        self.config.set("postgresql", "host", str(database_settings.host))
        self.config.set("postgresql", "database", str(database_settings.database))
        self.config.set("postgresql", "user", str(database_settings.user))
        self.config.set("postgresql", "password", str(database_settings.password))
        Config().save(self.config)

    def is_configured(self) -> bool:
        return Config().is_configured()

    def load(self):
        params = Config().load(self.config)
        host = params['host']
        database = params['database']
        user = params['user']
        password = params['password']
        database_settings = DatabaseSettings(host, database, user, password)
        return database_settings

    def get_db_version(self):
        version = 0
        if Config().section_exists("version") is True:
            config = Config().load(self.config)
            version = config["version"]
        else:
            version = 0.1
        return float(version)

    def set_db_version(self, version):
        if Config().section_exists("version") is False:
            self.config.add_section("version")
        self.config.set("version", "version", str(version))
        Config().save(self.config)
