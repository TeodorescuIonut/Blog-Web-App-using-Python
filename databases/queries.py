CREATE_POSTS_TABLE = """CREATE TABLE IF NOT EXISTS posts (post_id serial PRIMARY KEY,
        post_created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        post_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        post_title VARCHAR ( 255 ) NOT NULL,
        post_content VARCHAR NOT NULL);
"""
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY,
        user_date_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        user_date_modification TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        user_name VARCHAR ( 255 ) NOT NULL,
        user_email VARCHAR NOT NULL,
        user_password VARCHAR (255)) ;"""
ADD_OWNER_ID_COLUMN = "ALTER TABLE posts ADD COLUMN IF NOT EXISTS owner_id INTEGER;"
ADD_ADMIN_COLUMN = "ALTER TABLE users ADD COLUMN IF NOT EXISTS admin boolean;"
ADD_IMAGE_COLUMN = "ALTER TABLE posts ADD COLUMN IF NOT EXISTS image VARCHAR(255);"
ADD_COLUMN_POST_OWNER = "ALTER TABLE posts ADD COLUMN IF NOT EXISTS post_owner VARCHAR(255);"
LINK_POST_OWNER_TO_USER = """
DO
$$
BEGIN
    IF NOT EXISTS(SELECT * FROM pg_constraint WHERE conname = 'fk_user_id') THEN
        ALTER TABLE posts
        ADD CONSTRAINT fk_user_id 
        FOREIGN KEY (owner_id) 
        REFERENCES users(user_id) ON DELETE CASCADE;
    END IF;
END $$;    
"""

GENERATE_OWNER_IDS = """DO $$ DECLARE post record; BEGIN IF EXISTS(SELECT column_name FROM information_schema.columns 
WHERE table_name = 'posts' and column_name = 'post_owner') THEN FOR post IN SELECT * FROM posts LOOP IF 
post.post_owner IN (SELECT user_name FROM users) THEN UPDATE posts SET owner_id = (SELECT user_id FROM users WHERE 
user_name =post.post_owner) WHERE post_owner= post.post_owner; END IF; END LOOP; END IF; END; $$ """
GENERATE_USERS_FOR_POSTS = """DO $$ DECLARE post record; BEGIN IF EXISTS(SELECT column_name FROM 
information_schema.columns WHERE table_name = 'posts' and column_name = 'post_owner') THEN FOR post IN SELECT * FROM 
posts LOOP IF post.post_owner NOT IN (SELECT user_name FROM users) THEN INSERT INTO users (user_id, 
user_date_creation, user_date_modification,user_name, user_email, user_password) VALUES (DEFAULT, DEFAULT, DEFAULT, 
post.post_owner, post.post_owner, '1234'); END IF; END LOOP; END IF; END; $$ """
ADD_ADMIN_USER = """DO $$ BEGIN IF NOT EXISTS(SELECT user_name FROM users WHERE user_name = 'admin') THEN INSERT INTO 
users(user_date_creation, user_date_modification,user_name, user_email, user_password, admin) VALUES (DEFAULT, 
DEFAULT,'admin','admin@localhost.com', 
'sha256$rHEVul4CLa9kYwkm$6eace29a89092b5df84a8eea8aa2259c281b2f9c196331c1a5ce0afbe306626f', true); END IF; END; $$ """
GENERATE_NON_ADMINS = """DO $$ DECLARE user record; BEGIN FOR user IN SELECT * FROM users LOOP IF EXISTS(SELECT 
column_name from information_schema.columns WHERE table_name  = 'users' AND column_name ='admin') THEN UPDATE users 
SET admin= false WHERE admin IS NULL AND user_name <> 'admin'; END IF; END LOOP; END; $$ """
DELETE_POST_OWNER_COLUMN = """
ALTER TABLE posts DROP COLUMN post_owner;
"""
queries = [CREATE_POSTS_TABLE, CREATE_USERS_TABLE, ADD_COLUMN_POST_OWNER, ADD_IMAGE_COLUMN, GENERATE_USERS_FOR_POSTS,
           ADD_OWNER_ID_COLUMN,
           GENERATE_OWNER_IDS, LINK_POST_OWNER_TO_USER, ADD_ADMIN_COLUMN, ADD_ADMIN_USER, GENERATE_NON_ADMINS,
           DELETE_POST_OWNER_COLUMN]
