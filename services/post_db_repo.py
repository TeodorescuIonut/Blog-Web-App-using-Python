import sys
import os
from pathlib import Path

myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

from services.post_repository_interface import IPostRepository
from models.post_preview import PostPreview
from models.post import Post
from databases.database_manager import Database




class PostDbRepo(IPostRepository):
   
    def __init__(self):
        self.posts = list()
        self.db = Database()
    def create(self, post:Post):
        conn = self.db.create_conn()
        cur = conn.cursor()
        cur.execute(
                "INSERT INTO posts (post_title, post_content, post_owner) VALUES (%s, %s, %s) RETURNING post_id",
                (post.post_title, post.post_contents, post.post_owner),
            )
        conn.commit()
        post.post_id = cur.fetchone()[0]
        self.posts.append(post)
        self.db.close_and_save(conn)


    def get_all(self):
        conn = self.db.create_conn()
        cur = conn.cursor() 
        cur.execute("SELECT post_id,post_created_on,post_modified_on, post_title, LEFT(post_content, 500), post_owner  FROM posts ORDER BY post_created_on DESC")
        rows = cur.fetchall()[0]      
        for row in rows:
            post =Post("", "", "")
            post.post_id = row[0]
            post.post_date_creation = row[1]
            post.post_date_modification = row[2]
            post.post_title= row[3]
            post.post_contents= row[4]
            post.post_owner= row[5]
            if self.check_post_exists(post) is False:
                self.posts.append(post)
            conn.commit()
            conn.close()
        return self.posts

    def check_post_exists(self,post_to_check):
        for post in self.posts:
            if post.post_id == post_to_check.post_id:
                return True
        


    def get_by_id(self, post_id):
        conn = self.db.create_conn()
        cur = conn.cursor() 
        cur.execute('SELECT * FROM posts WHERE post_id = %s', (post_id,))
        data = cur.fetchall()[0]
        post =Post("", "", "")
        post.post_id = data[0]
        post.post_date_creation = data[1]
        post.post_date_modification = data[2]
        post.post_title= data[3]
        post.post_contents= data[4]
        post.post_owner= data[5]
        conn.commit()
        conn.close()
        return post
    def update(self, post:Post):
        conn = self.db.create_conn()
        cur = conn.cursor() 
        id = post.post_id
        index_post = self.get_post_index(id)
        self.posts.remove(self.posts[index_post])
        self.posts.append(post)      
        cur.execute("""
        UPDATE posts
        SET post_title = %s,
            post_content = %s,
            post_owner = %s
        WHERE post_id = %s RETURNING *
        """,(post.post_title, post.post_contents, post.post_owner, post.post_id))
        conn.commit()
        conn.close()
        
        
        
    
    def delete(self, post:Post):
        conn = self.db.create_conn()
        cur = conn.cursor()
        id = post.post_id 
        cur.execute('DELETE FROM posts WHERE post_id= %s', (id,)) 
        conn.commit()
        conn.close()
        index_post = self.get_post_index(id)
        self.posts.remove(self.posts[index_post])


    def get_post_index(self, id):
        for post in self.posts:
            if post.post_id == id:
                return self.posts.index(post)


    def get_previews(self):
        posts_previews = []
        posts = self.get_all()
        for post in posts:
            posts_previews.append(self.create_preview(post))
        return posts_previews

    def create_preview(self,post:Post):
        content_preview = post.post_contents[0:200]
        creation_date = post.post_date_creation
        modification_date = post.post_date_modification
        preview = PostPreview(post.post_id,post.post_title, content_preview, post.post_owner, creation_date, modification_date)
        return preview
    
