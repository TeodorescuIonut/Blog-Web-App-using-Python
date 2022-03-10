from databases.database_settings import DatabaseSettings
from interfaces.db_config_interface import IDatabaseConfig


class MemoryDatabaseConfig(IDatabaseConfig):
    config :True
        
    def save(self,database_settings:DatabaseSettings):
        pass
    

    def load(self):
        pass
    

    def is_configured(self):
        return self.set_configuration
    
    def set_configuration(self, config:bool):
        self.config = config
