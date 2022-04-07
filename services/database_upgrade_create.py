from interfaces.database_interface import IDatabase
from interfaces.database_upgrade_interface import IDatabaseUpgrade
from interfaces.db_config_interface import IDatabaseConfig
from databases.queries import queries


class DatabaseUpgradeAndCreate(IDatabaseUpgrade):

    def __init__(self, db: IDatabase, db_config: IDatabaseConfig):
        self.db = db
        self.version = 0.2
        self.db_config = db_config

    def is_latest_db_version(self):
        if self.version > self.db_config.get_db_version():
            return False

    def upgrade_db(self):
        conn = self.db.create_conn()
        curs = conn.cursor()
        if self.is_latest_db_version() is False:
            for query in queries:
                curs.execute(query)
                conn.commit()
            curs.close()
            conn.close()
            self.db_config.set_db_version(self.version)
