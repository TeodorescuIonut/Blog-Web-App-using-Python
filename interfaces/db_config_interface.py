import abc

from databases.database_settings import DatabaseSettings


class IDatabaseConfig(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self,database_settings:DatabaseSettings):
        raise NotImplementedError
    
    @abc.abstractmethod
    def load(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def is_configured(self):
        raise NotImplementedError