import datetime

from interfaces.image_repo_interface import IImageRepo
from interfaces.post_repository_interface import IPostRepository
from models.dtos.post_preview import PostPreview
from models.dtos.post import Post


class PostRepo(IPostRepository):
    posts = list()
    count = 0
    no_posts = 0

    def __init__(self, image_service: IImageRepo):
        self.image_service = image_service

    def get_all(self, per_page, offset, selected_owner_id) -> []:
        sorted_array = sorted(self.get_previews(selected_owner_id),
                              key=lambda x: x.created_at, reverse=True)
        self.no_posts = len(sorted_array)
        return sorted_array

    def get_by_id(self, post_id: int) -> Post:
        for post in self.posts:
            if post.id == post_id:
                return post

    def create(self, post, image_file):
        post.image = self.image_service.save_image(image_file)
        post.id = self.count
        format_data = '%B %d %Y %H:%M:%S'
        post.created_at = datetime.datetime.strptime(post.created_at, format_data)
        self.posts.append(post)
        self.count += 1

    def update(self, post: Post, image_file) -> None:
        self.posts.remove(post)
        if post.image is None:
            post.image = 'default.png'
        else:
            post.image = self.image_service.save_image(image_file)
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
                post.owner = updated_name

    def get_previews(self, selected_owner_id) -> []:
        posts_previews = []
        for post in self.posts:
            if post.owner_id == selected_owner_id:
                posts_previews.append(self.create_preview(post))
            elif selected_owner_id == -1:
                posts_previews.append(self.create_preview(post))
        return posts_previews

    @staticmethod
    def create_preview(post: Post):
        content_preview = post.contents[0:200]
        creation_date = post.created_at
        modification_date = post.modified_at
        preview = PostPreview(post.id, post.title,
                              content_preview, post.owner, creation_date, modification_date)
        return preview

    def get_post_index(self, owner_id) -> int:
        for post in self.posts:
            if owner_id == post.owner_id:
                return self.posts.index(post)
