import sys
import os
from pathlib import Path

from interfaces.db_config_interface import IDatabaseConfig
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from configparser import ConfigParser
from databases.database_settings import DatabaseSettings

class DatabaseConfig(IDatabaseConfig):
   
    def __init__(self):
        self.config = ConfigParser()
        self.file = 'database.ini'
        self.section = 'postgresql'
    
    def save(self, database_settings:DatabaseSettings):
        with open(self.file, "w", encoding='cp1251') as file:
            file.write(
            '[postgresql]\n'
            f'host = {database_settings.host}\n'
            f'database = {database_settings.database}\n'
            f'user = {database_settings.user}\n'
            f'password = {database_settings.password}'
            )
        
    def is_configured(self)->bool:
        return os.path.exists(f"./{self.file}")


        
    def load(self):
        params = self.__get_connection_settings()
        host = params['host']
        database = params['database']
        user = params['user']
        password = params['password']
        database_settings = DatabaseSettings(host,database, user,password)
        return database_settings
    
    def __get_connection_settings(self):
        parser = ConfigParser()
        parser.read(self.file)
        db = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f'Section {self.section} not found in {self.file}')
        return db