import sys
import os
from pathlib import Path

import pytest
from services.service import ContainerService
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
#pylint: disable=redefined-outer-name
from main import create_app
testing_app = create_app(test_config=True)

@pytest.fixture(name = "client")

def client():
    return testing_app.test_client()

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
    return client.get('/POST/VIEW/3')

def test_add_post(client):
    """Test if a new post can be added"""
    result =  add_post(client, "Hello world", "bla bla", "Jhon")
    resp = client.get('/POST/VIEW/0',follow_redirects=True)
    assert result.status == '200 OK'
    assert b"Hello World" in resp.data
    assert b"bla bla" in resp.data
    assert b"Jhon" in resp.data

def test_add_two_posts(client):
    """Test if a new post can be added"""
    result =  add_post(client, "Hello World", "bla bla", "Jhon")
    add_post(client, "Hello", "bla bla bla", "Peter")
    resp1 = client.get('/POST/VIEW/1',follow_redirects=True)
    resp2 = client.get('/POST/VIEW/2',follow_redirects=True)
    assert result.status == '200 OK'
    assert b"Hello World" in resp1.data
    assert b'bla bla' in resp1.data
    assert b"Jhon"  in resp1.data
    assert b"Hello" in resp2.data
    assert b"bla bla bla" in resp2.data
    assert b"Peter"  in resp2.data

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

def test_redirect_not_setup_false(client):
    ContainerService.memory_config.set_configuration = False
    response = client.get("/setup/",follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Host" in response.data
    assert b"Database" in response.data
    assert b"User" in response.data
    assert b"Password" in response.data
    assert b"Read about true experiences," not in response.data
    assert b"There are no blog posts." not in response.data
    response = client.get("/POST/",follow_redirects=True)
    assert b"Host" in response.data
    response = client.get("/POST/VIEW/1",follow_redirects=True)
    assert b"Host" in response.data
    response = client.get("/POST/UPDATE/1",follow_redirects=True)
    assert b"Host" in response.data
    response = client.get("/POST/DELETE/1",follow_redirects=True)
    assert b"Host" in response.data

def test_redirect_setup_true(client):
    ContainerService.memory_config.set_configuration = True
    response = client.get('/POST/', follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Read about true experiences," in response.data
    
