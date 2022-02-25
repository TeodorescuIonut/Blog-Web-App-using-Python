import sys
import os
from pathlib import Path
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
import psycopg2
from databases.database_config import DatabaseConfig



class Database:
    data_settings = DatabaseConfig().load()
    def create_conn(self):
        conn = psycopg2.connect(host = self.data_settings.host, database=self.data_settings.database, user = self.data_settings.user,password = self.data_settings.password)
        return conn
    def create_cursor(self):      
        conn = self.create_conn()
        cur = conn.cursor()
        return cur
    def create_table(self):
        cur = self.create_cursor()
        cur.execute(" DROP TABLE IF EXISTS posts;")
        cur.execute(' CREATE TABLE posts (post_id serial PRIMARY KEY,'
            'post_created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_title VARCHAR ( 255 ) NOT NULL,'
            'post_content VARCHAR NOT NULL,'
            'post_owner VARCHAR (255));')

    def close_and_save(self, conn):
        conn.commit()
        conn.close()
