from configparser import ConfigParser
import psycopg2

class PostDB:
    def __init__(self):
        params = self.config()
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()
    def query(self, query):
        self.cur.execute(query)
    def create_db(self):
        self.cur.execute(" DROP TABLE IF EXISTS posts;")
        self.cur.execute(' CREATE TABLE posts (post_id serial PRIMARY KEY,'
            'post_created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_title VARCHAR ( 255 ) NOT NULL,'
            'post_content VARCHAR NOT NULL,'
            'post_owner  );')
        self.conn.commit()
    def close(self):
        self.cur.close()
        self.cur.close()
    def config(self, filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db
