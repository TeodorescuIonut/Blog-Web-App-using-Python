from multiprocessing import connection
import sys
import os
from pathlib import Path

import psycopg2
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

from databases.database_config import DatabaseConfig



class Database:
    
    def create_conn(self):
        conn = None
        data_settings = DatabaseConfig().load()
        try:
            conn = psycopg2.connect(host = data_settings.host, database= data_settings.database, user = data_settings.user,password = data_settings.password)
        except(Exception, psycopg2.DatabaseError) as error:
            if(error):
                conn = psycopg2.connect(host = data_settings.host, user = data_settings.user,password = data_settings.password)
                conn.set_session(autocommit=True)
                conn.cursor().execute(f'CREATE DATABASE {data_settings.database}')
                conn.commit()
        finally:
            return conn
        
    def create_cursor(self):
        conn = self.create_conn()
        cur = conn.cursor()
        return cur
    def create_table(self):
        con = self.create_conn() 
        cur = con.cursor()
        cur.execute(" DROP TABLE IF EXISTS posts;")
        cur.execute(' CREATE TABLE posts (post_id serial PRIMARY KEY,'
            'post_created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_title VARCHAR ( 255 ) NOT NULL,'
            'post_content VARCHAR NOT NULL,'
            'post_owner VARCHAR (255));')
        cur.close()
        print('table created')
        con.commit()
        con.close()

    def close_and_save(self, conn):
        conn.commit()
        conn.close()
