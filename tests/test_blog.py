from pickle import TRUE
import sys
import os
from pathlib import Path
import pytest
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
#pylint: disable=redefined-outer-name
from app import app


@pytest.fixture(name = "client")
def client():
    app.config['TESTING']= TRUE
    return app.test_client()

def test_app(client):
    """Check an empty blog"""
    response = client.get('/POST/')
    assert response.status == '200 OK'
    assert b'There are no blog posts.' in response.data


def add_post(client,title, content, owner):
    return client.post('/POST/CREATE/posts', data = dict(
         title = title,
         owner = owner,
         content = content
    )
    , follow_redirects=True)

def delete_post(client):
    return client.post('/POST/DELETE/6', follow_redirects=True)

def update_post(client, title, content, owner):
    return client.post('/POST/UPDATE/1', data = dict(
         title = title,
         owner = owner,
         content = content
    )
    , follow_redirects=True)

def view_post(client):
    return client.get('/POST/')

def test_add_post(client):
    """Test if a new post can be added"""
    result =  add_post(client, "Hello world", "bla bla", "Jhon")
    resp = client.get('/POST/',follow_redirects=True)
    assert result.status == '200 OK'
    assert b"Hello World" in resp.data
    assert b"bla bla" in resp.data
    assert b"Jhon" in resp.data

def test_add_two_posts(client):
    """Test if a new post can be added"""
    result =  add_post(client, "Hello world", "bla bla", "Jhon")
    add_post(client, "Hello ", "bla bla bla", "Peter")
    resp = client.get('/POST/',follow_redirects=True)
    assert result.status == '200 OK'
    assert b"Hello World"
    assert b'bla bla' in resp.data
    assert b"Jhon"  in resp.data
    assert b"Hello" in resp.data
    assert b"bla bla bla" in resp.data
    assert b"Peter"  in resp.data

def test_view_post(client):
    """Test if a post can be viewed"""
    add_post(client,"Hello world", "bla bla", "Jhon")
    result = view_post(client)
    assert b'Hello World' in result.data
    assert b'bla bla' in result.data
    assert b'Jhon' in result.data


def test_update_post(client):
    """Test if a post can be updated"""
    add_post(client,"Hello world", "bla bla", "Jhon")
    add_post(client, "Hello ", "bla bla bla", "PEter")
    result = update_post(client, "Hello world update","bla bla update", "Jhon update")
    assert result.status == '200 OK'
    assert b'Hello world update' in result.data
    assert b'bla bla update' in result.data
    assert b'Jhon update' in result.data

def test_delete_post(client):
    """Test if a post can be deleted"""
    result = add_post(client,"Hell world", "new content", "Grace")
    result = delete_post(client)
    response = client.get('/POST/' , follow_redirects=True)
    assert b'Post deleted' in result.data
    assert b'Hell world' not in response.data
    assert b'new content' not in response.data
    assert b'Grace' not in response.data
