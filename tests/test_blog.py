import json
from pdb import post_mortem
from sys import prefix
from turtle import pos

import flask

from flask import Flask
from models.Post import Post
from PostsRepo.postRepo import postRepo
from app import app
from routes.post_bp import post_bp
import pytest

@pytest.fixture
def client():
     return app.test_client()

def test_app(client):
        """Check an empty blog"""
        rv = client.get('/POST/')
        assert rv.status == '200 OK'
        assert b'There are no blog posts.' in rv.data


def addPost(client,title, content, owner):
    return client.post('/POST/CREATE/posts', data = dict(
         title = title,
         owner = owner,
         content = content
    )
    , follow_redirects=True)

def updatePost(client, title, content, owner):
    return client.post('/POST/UPDATE/0', data = dict(
         title = title,
         owner = owner,
         content = content
    )
    , follow_redirects=True)

def deletePost(client):
     return client.post('/POST/DELETE/0', follow_redirects=True)

def viewPost(client):
     return client.post('/POST/VIEW/0')

def test_add_post(client):
     """Test if a new post can be added"""
     result =  addPost(client, "Hello world", "bla bla", "Jhon")
     assert result.status == '200 OK'
     assert b'Post added' in result.data
def test_view_post(client):
     """Test if a post can be viewed"""
     addPost(client,"Hello world", "bla bla", "Jhon")
     result = viewPost(client)
     assert b'Hello World' in result.data


def test_update_post(client):
     """Test if a post can be updated"""
     addPost(client,"Hello world", "bla bla", "Jhon")
     result = updatePost(client, "Hello world update","bla bla", "Jhon")
     assert result.status == '200 OK'
     assert b'Hello world update' in result.data

def test_delete_post(client):
     """Test if a post can be deleted"""
     addPost(client,"Hello world", "bla bla", "Jhon")
     result = deletePost(client)
     assert b'Post deleted' in result.data


