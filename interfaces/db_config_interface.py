import abc

from databases.database_settings import DatabaseSettings


class IDatabaseConfig(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self,database_settings:DatabaseSettings):
        pass
    
    @abc.abstractmethod
    def load(self):
        pass
    
    @abc.abstractmethod
    def is_configured(self):
        pass

    @abc.abstractmethod
    def get_db_version(self):
        pass

    @abc.abstractmethod
    def set_db_version(self, version):
        pass