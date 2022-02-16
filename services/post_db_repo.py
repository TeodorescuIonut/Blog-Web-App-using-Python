from services.post_repository_interface import IPostRepository
from models.post_preview import PostPreview
from models.post import Post
from post_db import PostDB

db = PostDB()

class PostDbRepo(IPostRepository):

    def __init__(self):
        self.posts = list()
        self.count = 0

    def create(self, post):      
        db.cur.execute(
                "INSERT INTO posts (post_title, post_content, post_owner) VALUES (%s, %s, %s) RETURNING post_id",
                (post.post_title, post.post_contents, post.post_owner),
            )
        post.post_id = db.cur.fetchone()[0]
        db.conn.commit()


    def get_all(self):
        db.cur.execute("SELECT * FROM posts")
        rows = db.cur.fetchall()        
        for row in rows:
            post =Post("", "", "")
            post.post_id = row[0]
            post.post_date_creation = row[1]
            post.post_date_modification = row[2]
            post.post_title= row[3]
            post.post_contents= row[4]
            post.post_owner= row[5]
            self.posts.append(post)
        return self.posts

    def get_by_id(self, post_id):
        db.cur.execute('SELECT * FROM posts WHERE post_id = %s', (post_id,))
        data = db.cur.fetchall()[0]
        print(data)
        post =Post("", "", "")
        post.post_id = data[0]
        post.post_date_creation = data[1]
        post.post_date_modification = data[2]
        post.post_title= data[3]
        post.post_contents= data[4]
        post.post_owner= data[5]
        return post
    def update(self, post):
        self.posts.append(post)
        db.cur.execute("""
        UPDATE posts
        SET post_title = %s,
            post_content = %s,
            post_owner = %s
        WHERE post_id = %s RETURNING *
        """,(post.post_title, post.post_contents, post.post_owner, post.post_id))
        self.posts.remove(post)
        
    
    def delete(self, post):       
        db.cur.execute('DELETE FROM posts WHERE post_id= {0}'.format(post.post_id))
        db.conn.commit()
        
    def get_previews(self):
        posts_previews = []
        posts = self.get_all()
        for post in posts:
            posts_previews.append(self.create_preview(post))
        return posts_previews

    def create_preview(self,post):
        content_preview = post.post_contents[0:200]
        creation_date = post.post_date_creation
        modification_date = post.post_date_modification
        preview = PostPreview(post.post_id,post.post_title, content_preview, post.post_owner, creation_date, modification_date)
        return preview
    
    def check_post(self, post, posts):
        for ex_post in posts:
            if post.post_id == ex_post.post_id:
                return True


