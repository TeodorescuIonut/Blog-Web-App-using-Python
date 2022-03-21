import configparser
import sys
import os
from pathlib import Path
from interfaces.database_interface import IDatabase
from interfaces.database_upgrade_interface import IDatabaseUpgrade

myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from databases.queries import queries



class DatabaseUpgradeandCreate(IDatabaseUpgrade):

    def __init__(self, db:IDatabase):
        self.db = db
        self.version = 0.2

    def upgrade_db(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read('database.ini')
        version = config.get("postgresql", "version") if config.has_option("postgresql", "version") else 0.1
        conn = self.db.create_conn()
        curs = conn.cursor()
        if self.version > float(version):
            config.set("postgresql", "version",str(self.version))
            with open('database.ini', 'w',encoding='cp1251') as configfile:
                config.write(configfile)
            for query in queries:
                curs.execute(query)
                conn.commit()
            curs.close()
            conn.close()