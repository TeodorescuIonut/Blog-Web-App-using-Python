import sys
import os
from pathlib import Path


myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

from interfaces.post_repository_interface import IPostRepository
from models.post import Post
from interfaces.database_interface import IDatabase

class PostDbRepo(IPostRepository):
    posts = list()
    def __init__(self, db:IDatabase):
        self.db = db
    def create(self, post:Post) -> None:
        conn = self.db.create_conn()
        cur = conn.cursor()
        cur.execute(
                "INSERT INTO posts (post_title, post_content, owner_id) VALUES (%s, %s, %s) RETURNING post_id",
                (post.post_title, post.post_contents, post.owner_id),
            )
        post.post_id = cur.fetchone()[0]
        self.posts.append(post)
        self.db.close_and_save(conn,cur)


    def get_all(self) -> list():
        conn = self.db.create_conn()
        cur = conn.cursor() 
        cur.execute("SELECT post_id,post_created_on,post_modified_on, post_title, LEFT(post_content, 500), owner_id, user_name   FROM posts INNER JOIN users ON owner_id = user_id ORDER BY post_created_on DESC")
        rows = cur.fetchall()
        for row in rows:
            post =Post("", "","","")
            post.post_id = row[0]
            post.post_date_creation = row[1]
            post.post_date_modification = row[2]
            post.post_title= row[3]
            post.post_contents= row[4]
            post.owner_id= row[5]
            post.post_owner = row[6]
            if self.check_post_exists(post) is False:
                self.posts.append(post)
        self.db.close_and_save(conn, cur)
        return self.posts

    def check_post_exists(self,post_to_check:Post)-> bool:
        if len(self.posts) > 0:
            for post in self.posts:
                if post_to_check.post_id == post.post_id:
                    return True
        return False
        
    def get_by_id(self, post_id:int) -> Post:
        conn = self.db.create_conn()
        cur = conn.cursor() 
        cur.execute("SELECT post_id, to_char(post_created_on, 'dd/mm/yyyy HH24:MI'),to_char(post_modified_on, 'dd/mm/yyyy HH24:MI'), post_title, post_content, owner_id, user_name  FROM posts INNER JOIN users ON owner_id = user_id  WHERE post_id = %s", (post_id,))
        data = cur.fetchone()
        post =Post("", "", "","")
        post.post_id = data[0]
        post.post_date_creation = data[1]
        post.post_date_modification = data[2]
        post.post_title= data[3]
        post.post_contents= data[4]
        post.owner_id= data[5]
        post.post_owner = data[6]
        self.db.close_and_save(conn, cur)
        return post
    def update(self, post:Post) -> None:
        conn = self.db.create_conn()
        cur = conn.cursor() 
        id = post.post_id
        index_post = self.get_post_index(id)
        self.posts.remove(self.posts[index_post])
        self.posts.append(post)      
        cur.execute("""
        UPDATE posts
        SET post_title = %s,
            post_content = %s
        WHERE post_id = %s RETURNING *
        """,(post.post_title, post.post_contents, post.post_id))
        self.db.close_and_save(conn, cur)     
    
    def delete(self, post:Post) -> None:
        conn = self.db.create_conn()
        cur = conn.cursor()
        id = post.post_id 
        cur.execute('DELETE FROM posts WHERE post_id= %s', (id,)) 
        self.db.close_and_save(conn, cur)
        index_post = self.get_post_index(id)
        if index_post is not None:
            self.posts.remove(self.posts[index_post])


    def get_post_index(self, id: int)-> int:
        for post in self.posts:
            if post.post_id == id:
                return self.posts.index(post)
    
