import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        print(cur)
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute(" DROP TABLE IF EXISTS posts;")
        cur.execute(' CREATE TABLE posts (post_id serial PRIMARY KEY,'
            'post_created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            'post_title VARCHAR ( 255 ) NOT NULL,'
            'post_content VARCHAR NOT NULL,'
            'post_owner VARCHAR ( 50 ) UNIQUE NOT NULL);')
        cur.execute('INSERT INTO posts (post_title, post_content, post_owner)'
            'VALUES (%s, %s, %s)',
            ('A Tale of Two Cities',
             'A great classic!',
             'Charles Dickens')
            )
        conn.commit()
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()