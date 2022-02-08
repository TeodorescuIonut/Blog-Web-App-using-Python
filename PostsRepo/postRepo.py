from operator import imod
import re
from turtle import pos
from IPostRepository import IPostRepository

class postRepo(IPostRepository):
    def __init__(self):
        self.posts = list()
        self.count = 0
    
    def getAll(self):
        return self.posts

    def getById(self, id):
        for post in self.posts:
            if post.postId == id:
                return post
    
    def create(self, post):
        post.postId = self.count
        self.posts.append(post)
        self.count +=1
    
    def update(self, post):
        self.posts.remove(post)
        self.posts.append(post)

    def delete(self, post):
        self.posts.remove(post)

print(postRepo.__mro__)