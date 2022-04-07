from interfaces.post_repository_interface import IPostRepository
from models.post_preview import PostPreview
from models.post import Post


class PostRepo(IPostRepository):
    posts = list()
    count = 0
    no_posts = 0

    def get_all(self, per_page, offset, selected_owner_id) -> []:
        sorted_array = sorted(self.get_previews(selected_owner_id), key=lambda x: x.post_date_creation, reverse=True)
        self.no_posts = len(sorted_array)
        return sorted_array

    def get_by_id(self, post_id: int) -> Post:
        for post in self.posts:
            if post.post_id == post_id:
                return post

    def create(self, post):
        post.post_id = self.count
        self.posts.append(post)
        self.count += 1

    def update(self, post: Post) -> None:
        self.posts.remove(post)
        self.posts.append(post)

    def delete(self, post: Post) -> None:
        self.posts.remove(post)
        self.count -= 1

    def delete_all_user_posts(self, owner_id):
        i = len(self.posts)
        while i:
            i -= 1
            if owner_id == self.posts[i].owner_id:
                del self.posts[i]

    def update_users_posts(self, updated_name, user_id):
        for post in self.posts:
            if post.owner_id == user_id:
                post.post_owner = updated_name

    def get_previews(self, selected_owner_id) -> []:
        posts_previews = []
        for post in self.posts:
            if post.owner_id == selected_owner_id:
                posts_previews.append(self.create_preview(post))
            elif selected_owner_id == -1:
                posts_previews.append(self.create_preview(post))
        return posts_previews

    @staticmethod
    def create_preview(post: PostPreview):
        content_preview = post.post_contents[0:200]
        creation_date = post.post_date_creation
        modification_date = post.post_date_modification
        preview = PostPreview(post.post_id, post.post_title,
                              content_preview, post.post_owner, creation_date, modification_date)
        return preview

    def get_post_index(self, owner_id) -> int:
        for post in self.posts:
            if owner_id == post.owner_id:
                return self.posts.index(post)
