from interfaces.image_repo_interface import IImageRepo
from interfaces.post_repository_interface import IPostRepository
from interfaces.database_interface import IDatabase
from models.post import Post


class PostDbRepo(IPostRepository):
    posts = list()
    no_posts = 0

    def __init__(self, database: IDatabase, image_service: IImageRepo):
        self.database = database
        self.image_service = image_service

    def create(self, post: Post, image_file) -> None:
        conn = self.database.create_conn()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO posts (post_title,
                                  post_content,
                                  owner_id,
                                  image)
                VALUES (%s, %s, %s, %s) RETURNING post_id""",
            (post.post_title, post.post_contents, post.owner_id, image_file.filename),
        )
        post.post_id = cur.fetchone()[0]
        self.posts.append(post)
        if image_file.filename != '':
            image_file.filename = str(post.post_id) + image_file.filename
        self.image_service.save_image(image_file, image_file.filename)
        cur.execute("""
                UPDATE posts
                SET
                    image = %s
                WHERE post_id = %s
                """, (image_file.filename, post.post_id))
        self.database.close_and_save(conn, cur)

    def get_all(self, per_page, offset, selected_owner_id) -> []:
        conn = self.database.create_conn()
        cur = conn.cursor()
        query = ""
        if selected_owner_id != -1:
            query = f"WHERE owner_id = {selected_owner_id}"
        cur.execute(
            f"""SELECT post_id,
                       post_created_on,
                       post_modified_on,
                       post_title,
                       LEFT(post_content, 500),
                       owner_id,
                       image,
                       user_name,
                       COUNT(*) OVER() AS full_count
                FROM posts INNER JOIN users ON owner_id = user_id {query}
                ORDER BY post_created_on DESC OFFSET {offset}  LIMIT {per_page}""")
        rows = cur.fetchall()
        self.posts.clear()
        self.no_posts = len(rows)
        if len(rows) > 0:
            self.no_posts = rows[0][8]
        for row in rows:
            post = Post("", "", "", "")
            post.post_id = row[0]
            post.post_date_creation = row[1]
            post.post_date_modification = row[2]
            post.post_title = row[3]
            post.post_contents = row[4]
            post.owner_id = row[5]
            post.image = row[6]
            post.post_owner = row[7]
            if self.check_post_exists(post) is False:
                self.posts.append(post)
        self.database.close_and_save(conn, cur)
        return self.posts

    def check_post_exists(self, post_to_check: Post) -> bool:
        if len(self.posts) > 0:
            for post in self.posts:
                if post_to_check.post_id == post.post_id:
                    return True
        return False

    def get_by_id(self, post_id: int) -> Post:
        conn = self.database.create_conn()
        cur = conn.cursor()
        cur.execute(
            """SELECT post_id,
                      to_char(post_created_on, 'dd/mm/yyyy HH24:MI'),
                      to_char(post_modified_on, 'dd/mm/yyyy HH24:MI'),
                      post_title,
                      post_content,
                      owner_id,
                      image,
                      user_name
                FROM posts INNER JOIN users ON owner_id = user_id
                WHERE post_id = %s""",
            (post_id,))
        data = cur.fetchone()
        post = Post("", "", "", "")
        if data is not None:
            post.post_id = data[0]
            post.post_date_creation = data[1]
            post.post_date_modification = data[2]
            post.post_title = data[3]
            post.post_contents = data[4]
            post.owner_id = data[5]
            post.image = data[6]
            post.post_owner = data[7]
            self.database.close_and_save(conn, cur)
        else:
            post = None
        return post

    def update(self, post: Post, image_file) -> None:
        conn = self.database.create_conn()
        cur = conn.cursor()
        id_post = post.post_id
        index_post = self.get_post_index(id_post)
        self.posts.remove(self.posts[index_post])
        self.posts.append(post)
        if image_file.filename != '' and str(post.post_id) + image_file.filename != post.image:
            image_file.filename = str(post.post_id) + image_file.filename
            self.image_service.save_image(image_file, image_file.filename)
            self.image_service.remove_image(post.image)
            post.image = image_file.filename
        cur.execute("""
        UPDATE posts
        SET post_title = %s,
            post_content = %s,
            image = %s
        WHERE post_id = %s RETURNING *
        """, (post.post_title, post.post_contents, post.image, post.post_id))
        self.database.close_and_save(conn, cur)

    def delete(self, post: Post) -> None:
        conn = self.database.create_conn()
        cur = conn.cursor()
        id_post = post.post_id
        cur.execute('DELETE FROM posts WHERE post_id= %s', (id_post,))
        self.database.close_and_save(conn, cur)
        index_post = self.get_post_index(id_post)
        self.image_service.remove_image(post.image)
        if index_post is not None:
            self.posts.remove(self.posts[index_post])

    def get_post_index(self, id_post: int) -> int:
        for post in self.posts:
            if post.post_id == id_post:
                return self.posts.index(post)
