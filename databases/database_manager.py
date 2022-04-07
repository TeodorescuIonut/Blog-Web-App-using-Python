import psycopg2
from interfaces.database_interface import IDatabase
from interfaces.db_config_interface import IDatabaseConfig




class Database(IDatabase):
    def __init__(self, db_config:IDatabaseConfig):
        self.db_config = db_config

    def create_conn(self):
        conn = None
        data_settings = self.db_config.load()
        conn = psycopg2.connect(host = data_settings.host,
                                database = data_settings.database,
                                user = data_settings.user,
                                password = data_settings.password)
        return conn

    def create_cursor(self):
        conn = self.create_conn()
        cur = conn.cursor()
        return cur
    def check_table_exists(self, table_name)-> bool:
        con = self.create_conn()
        cur = con.cursor()
        result = cur.execute(
            """SELECT EXISTS (SELECT relname FROM pg_class WHERE relname = %s);""",(table_name,))
        return result
    def close_and_save(self, conn,cur):
        conn.commit()
        cur.close()
        conn.close()
