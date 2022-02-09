
class PostRepo():
    def __init__(self):
        self.posts = list()
        self.count = 0
    def get_all(self):
        return self.posts

    def get_by_id(self, post_id):
        for post in self.posts:
            if post.post_id == post_id:
                return post
    def create(self, post):
        post.post_id = self.count
        self.posts.append(post)
        self.count += 1
    def update(self, post):
        self.posts.remove(post)
        self.posts.append(post)

    def delete(self, post):
        self.posts.remove(post)
