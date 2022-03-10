import sys
import os
from pathlib import Path


import psycopg2
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)


from interfaces.database_interface import IDatabase
from interfaces.db_config_interface import IDatabaseConfig




class Database(IDatabase):
    def __init__(self, db_config:IDatabaseConfig):
        self.db_config = db_config

    def create_conn(self):
        conn = None
        data_settings = self.db_config.load()
        try:
            conn = psycopg2.connect(host = data_settings.host,database = data_settings.database, user = data_settings.user,password = data_settings.password)
        except(Exception, psycopg2.DatabaseError) as error:
            if(error):           
                print(error)
        finally:
            return conn
        
    def create_cursor(self):
        conn = self.create_conn()
        cur = conn.cursor()
        return cur
    def create_table(self):
        con = self.create_conn() 
        cur = con.cursor()
        cur.execute(' CREATE TABLE IF NOT EXISTS posts (post_id serial PRIMARY KEY,'
            'post_created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_title VARCHAR ( 255 ) NOT NULL,'
            'post_content VARCHAR NOT NULL,'
            'post_owner VARCHAR (255)) ;')
        self.close_and_save(con, cur)

    def close_and_save(self, conn,cur):
        conn.commit()
        cur.close()
        conn.close()
