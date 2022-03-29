
import pytest
from services.service import ContainerService
from main import create_app
testing_app = create_app(test_config=True)

@pytest.fixture(name = "client")

def test_client():
    return testing_app.test_client()

def test_app(client):
    """Check an empty blog"""
    response = client.get('/POST/')
    assert response.status == '200 OK'

def sign_in_user(client, email, password):
    return client.post('/SIGNIN/', data = dict(
         email = email,
         password = password
    )
    , follow_redirects=True)

def sign_out_user(client):
    return client.get('/SIGNOUT/', follow_redirects=True)


def add_post(client,title, content, owner, owner_id):
    return client.post('/POST/CREATE/posts', data = dict(
         title = title,
         owner = owner,
         content = content,
         owner_id = owner_id
    )
    , follow_redirects=True)

def delete_post(client):
    return client.post('/POST/DELETE/12', follow_redirects=True)

def update_post(client, title, content, owner):
    return client.post('/POST/UPDATE/11', data = dict(
         title = title,
         owner = owner,
         content = content
    )
    , follow_redirects=True)
def add_user(client,name, email, password):
    return client.post('/USER/CREATE/users', data = dict(
         name = name,
         email = email,
         password = password
    )
    , follow_redirects=True)
def view_post(client):
    return client.get('/POST/VIEW/11')

def test_add_post(client):
    """Test if a new post can be added"""
    sign_in_user(client, "admin@localhost.com", "1234")
    add_user(client, "Peters", "blasss@yahoo.com", "1234")
    sign_out_user(client)
    sign_in_user(client, "blasss@yahoo.com", "1234")
    result =  add_post(client, "Hello world", "bla bla", "Peters", 2)
    resp = client.get('/POST/VIEW/8',follow_redirects=True)
    assert result.status == '200 OK'
    assert b"Hello World" in resp.data
    assert b"bla bla" in resp.data
    assert b"Peters" in resp.data

def test_add_two_posts(client):
    """Test if a new post can be added"""
    sign_in_user(client, "blasss@yahoo.com", "1234")
    result =  add_post(client, "Hello World", "bla bla", "Peters", 1)
    add_post(client, "Hello", "bla bla bla", "Peters", 1)
    resp1 = client.get('/POST/VIEW/12',follow_redirects=True)
    resp2 = client.get('/POST/VIEW/13',follow_redirects=True)
    assert result.status == '200 OK'
    assert b"Hello World" in resp1.data
    assert b'bla bla' in resp1.data
    assert b"Peters"  in resp1.data
    assert b"Hello" in resp2.data
    assert b"bla bla bla" in resp2.data
    assert b"Peters"  in resp2.data

def test_view_post(client):
    """Test if a post can be viewed"""
    sign_in_user(client, "blasss@yahoo.com", "1234")
    add_post(client,"Hello world", "bla bla", "Peters", 1)
    result = view_post(client)
    assert b'Hello World' in result.data
    assert b'bla bla' in result.data
    assert b'Peters' in result.data


def test_update_post(client):
    """Test if a post can be updated"""
    sign_in_user(client, "blasss@yahoo.com", "1234")
    add_post(client,"Hello world", "bla bla",'Peters', 1)
    result = update_post(client, "Hello world update","bla bla update","Peters")
    assert result.status == '200 OK'
    assert b'Hello world update' in result.data
    assert b'bla bla update' in result.data
    assert b'Peters' in result.data

def test_delete_post(client):
    """Test if a post can be deleted"""
    sign_in_user(client, "blasss@yahoo.com", "1234")
    result = add_post(client,"Hell world", "new content", "Peters",1)
    result = delete_post(client)
    response = client.get('/POST/' , follow_redirects=True)
    assert b'Post deleted' in result.data
    assert b'Hell world' not in response.data
    assert b'new content' not in response.data

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
    
