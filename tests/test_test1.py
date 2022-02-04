from pdb import post_mortem
from turtle import pos
from models.Post import Post
from PostsRepo.postRepo import postRepo
from app import app
import pytest

class TestClass:
   def test_new_post(self):
        """
        GIVEN a Post model
        WHEN a new post is created
        THEN check the post attributes
        """
        post = Post("Hello World","bla bla bla","jhon")
        assert post.postTitle == 'Hello World'
        assert post.postContents == 'bla bla bla'
        assert post.postOwner == "jhon"
   
   def test_create_post(self):
        """
        GIVEN a Post list
        WHEN a new post is created
        THEN check if the post was added to the posts list
        """
        post = Post("Hello World","bla bla bla","jhon")
        myList = postRepo()
        myList.create(post)
        assert myList.posts[0] == post

   def test_getAll_posts(self):
        """
        GIVEN a Post list
        WHEN posts are requested
        THEN get all the posts that were added to the posts list
        """
        post1 = Post("Hello World","bla bla bla","jhon")
        post2 = Post("Hello World!","bla bla bla","Brian")
        myList = postRepo()
        myList.create(post1)
        myList.create(post2)
        assert len(myList.posts) == 2
   
   def test_getID_post(self):
        """
        GIVEN a Post list
        WHEN a post ID is requested
        THEN get post by ID number
        """
        post1 = Post("Hello World","bla bla bla","jhon")
        post2 = Post("Hello World!","bla bla bla","Brian")
        myList = postRepo()
        myList.create(post1)
        myList.create(post2)
        assert myList.getById(0) == post1

   def test_delete_post(self):
        """
        GIVEN a Post list
        WHEN a post is deleted
        THEN check if the post was deleted
        """
        post1 = Post("Hello World","bla bla bla","jhon")
        myList = postRepo()
        myList.create(post1)
        myList.delete(post1)
        assert len(myList.posts) == 0

   def test_update_post(self):
        """
        GIVEN a Post list
        WHEN a post is updated
        THEN check if the post was updated
        """
        post1 = Post("Hello World","bla bla bla","jhon")
        myList = postRepo()
        myList.create(post1)
        post1.postTitle = "Hello again"
        myList.update(post1)
        assert myList.posts[0].postTitle == "Hello again"

@pytest.fixture(scope='module')
def new_post():
    post = Post("Hello World","bla bla bla","jhon")
    return post

def test_new_post_with_fixture(new_post):
    """
    GIVEN a Post model
    WHEN a new post is created
    THEN check the e
    """
    assert new_post.postTitle == 'Hello World'
    assert new_post.postContents == 'bla bla bla'
    assert new_post.postOwner == "jhon"