import sys
import os
from pathlib import Path
myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from configparser import ConfigParser
from databases.database_settings import DatabaseSettings

class DatabaseConfig:
    def __init__(self):
        self.config = ConfigParser()
        self.config['postgresql'] = {}
        self.section = self.config['postgresql']
    
    def save(self,host, database, user,password):
        database_settings = DatabaseSettings(host,database, user,password)
        self.section = self.config['postgresql']
        self.section['host'] = database_settings.host
        self.section['database'] = database_settings.database
        self.section['user'] = database_settings.user
        self.section['password'] = database_settings.password
        with open("database.ini", "w", encoding='cp1251') as my_file:
            self.config.write(my_file)
    def is_configured(self):
        if not os.path.exists("./database.ini"):
            return False

        
    def load(self):
        section = self.config['postgresql']
        host = section.get('host')
        database = section.get('database')
        user = section.get('user')
        password = section.get('password')
        return DatabaseSettings(host,database, user,password)