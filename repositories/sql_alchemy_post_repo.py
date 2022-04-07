from sqlalchemy import func,case,insert,update,delete,desc
from interfaces.databse_sqlalchemy_interface import IDatabaseAlchemy
from interfaces.post_repository_interface import IPostRepository
from models.post import Post
from models.post_sqlalchemy import PostSQLAlchemy
from models.user_sqlalchemy import UserSQLAlchemy


class SQLAlchemyPostRepo(IPostRepository):
    posts = list()
    no_posts = 0
    def __init__(self, database:IDatabaseAlchemy):
        self.database = database

    def get_all(self,per_page, offset, selected_owner_id):
        conn = self.database.create_conn()
        res  = conn.query(PostSQLAlchemy.post_id,
        PostSQLAlchemy.post_date_creation,
        PostSQLAlchemy.post_date_modification,
        PostSQLAlchemy.post_title,
        func.count(PostSQLAlchemy.post_id).over().label('total'),
        func.substr(PostSQLAlchemy.post_contents,0,100),
        UserSQLAlchemy.user_name).\
        join(UserSQLAlchemy).\
        filter(case([(selected_owner_id != -1,PostSQLAlchemy.owner_id == selected_owner_id )],
        else_=PostSQLAlchemy.owner_id > 0)).\
        order_by(desc(PostSQLAlchemy.post_date_creation)).\
        offset(offset).limit(per_page).all()
        self.posts.clear()
        self.no_posts = len(res)
        if len(res) > 0:
            self.no_posts = res[0][4]
        for row in res:
            post =Post("", "","","")
            post.post_id = row[0]
            post.post_date_creation = row[1]
            post.post_date_modification = row[2]
            post.post_title= row[3]
            post.post_contents= row[5]
            post.post_owner = row[6]
            if self.check_post_exists(post) is False:
                self.posts.append(post)
        self.database.close_and_save(conn)
        return self.posts

    def check_post_exists(self,post_to_check:Post)-> bool:
        if len(self.posts) > 0:
            for post in self.posts:
                if post_to_check.post_id == post.post_id:
                    return True
        return False

    def get_by_id(self, post_id):
        conn = self.database.create_conn()
        res = conn.query(PostSQLAlchemy,UserSQLAlchemy.user_name).\
        join(UserSQLAlchemy).filter(PostSQLAlchemy.post_id == post_id).first()
        if res is None:
            return None
        post = Post(res[1],res[0].post_title, res[0].post_contents,res[0].owner_id, res[0].post_id)
        self.database.close_and_save(conn)
        return post


    def create(self, post:Post):
        conn = self.database.create_conn()
        posts_table = PostSQLAlchemy.__table__
        stmt = (insert(posts_table).\
        values(post_title = post.post_title,
        post_content =post.post_contents,
        owner_id = post.owner_id ).\
        returning(posts_table.c.post_id))
        res = conn.execute(stmt).first()[0]
        post.post_id = res
        self.database.close_and_save(conn)

    def update(self, post:Post):
        conn = self.database.create_conn()
        posts_table = PostSQLAlchemy.__table__
        stmt = (update(posts_table).where(posts_table.c.post_id == post.post_id).\
        values(post_title = post.post_title, post_content = post.post_contents))
        conn.execute(stmt)
        self.database.close_and_save(conn)

    def delete(self, post):
        conn= self.database.create_conn()
        posts_table = PostSQLAlchemy.__table__
        stmt = (delete(posts_table).where(posts_table.c.post_id == post.post_id))
        conn.execute(stmt)
        self.database.close_and_save(conn)
