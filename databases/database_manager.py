from configparser import ConfigParser
import psycopg2

class Database:
    configured = False
    host= 'localhost'
    database='suppliers'
    user='postgres'
    password ='8211234'
    
    def get_con_details(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def create_conn(self):
        params = self.config()
        conn = psycopg2.connect(**params)
        return conn
    def create_cursor(self, conn):
        cur = conn.cursor()
        return cur
    def create_table(self):
        conn = self.create_conn()
        cur = self.create_cursor(conn)
        cur.execute(" DROP TABLE IF EXISTS posts;")
        cur.execute(' CREATE TABLE posts (post_id serial PRIMARY KEY,'
            'post_created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_title VARCHAR ( 255 ) NOT NULL,'
            'post_content VARCHAR NOT NULL,'
            'post_owner VARCHAR (255));')
        conn.commit()
        self.close(cur, conn)
    def close(self, cur, conn):
        conn.close()
        cur.close()
    def config(self):
        # create a parser
        parser = ConfigParser()
        parser.add_section("postgresql")
        section = "postgresql"
        parser.set("postgresql", "host",self.host)
        parser.set("postgresql", "database",self.database)
        parser.set("postgresql", "user",self.user)
        parser.set("postgresql", "password",self.password)
        cfgfile = open("databases/database.ini",'w', encoding='UTF-8')
        parser.write(cfgfile)

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, cfgfile))

        return db
