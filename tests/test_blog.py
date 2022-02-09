import pytest
#pylint: disable=redefined-outer-name
from app import app


@pytest.fixture(name = "client")
def client():
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

def update_post(client, title, content, owner):
    return client.post('/POST/UPDATE/0', data = dict(
         title = title,
         owner = owner,
         content = content
    )
    , follow_redirects=True)

def delete_post(client):
    return client.post('/POST/DELETE/0', follow_redirects=True)

def view_post(client):
    return client.post('/POST/VIEW/0')

def test_add_post(client):
    """Test if a new post can be added"""
    result =  add_post(client, "Hello world", "bla bla", "Jhon")
    assert result.status == '200 OK'
    assert b'Post added' in result.data

def test_view_post(client):
    """Test if a post can be viewed"""
    add_post(client,"Hello world", "bla bla", "Jhon")
    result = view_post(client)
    assert b'Hello World' in result.data


def test_update_post(client):
    """Test if a post can be updated"""
    add_post(client,"Hello world", "bla bla", "Jhon")
    result = update_post(client, "Hello world update","bla bla", "Jhon")
    assert result.status == '200 OK'
    assert b'Hello world update' in result.data

def test_delete_post(client):
    """Test if a post can be deleted"""
    add_post(client,"Hello world", "bla bla", "Jhon")
    result = delete_post(client)
    assert b'Post deleted' in result.data
    