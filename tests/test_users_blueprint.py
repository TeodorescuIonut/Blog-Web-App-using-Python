import pytest
from services.service import ContainerService
from main import create_app
testing_app = create_app(test_config=True)

@pytest.fixture(name = "client")

def test_client():
    return testing_app.test_client()

def test_app(client):
    sign_in_user(client, "admin@localhost.com", "1234")
    response = client.get('/USER/')
    assert response.status == '200 OK'

def sign_in_user(client, email, password):
    return client.post('/SIGNIN/', data = dict(
         email = email,
         password = password
    )
    , follow_redirects=True)
def add_user(client,name, email, password):
    return client.post('/USER/CREATE/users', data = dict(
         name = name,
         email = email,
         password = password
    )
    , follow_redirects=True)

def delete_user(client):
    return client.post('/USER/DELETE/9', follow_redirects=True)

def update_user(client, name, email, password):
    return client.post('/USER/UPDATE/2', data = dict(
         name = name,
         email = email,
         password = password
    )
    , follow_redirects=True)

def view_user(client):
    return client.get('/USER/VIEW/7')

def test_add_user(client):
    """Test if a new post can be added"""
    sign_in_user(client, "admin@localhost.com", "1234")
    result =  add_user(client, "Jhonny", "Jhonny@yahoo.com", "1234")
    resp = client.get('/USER/VIEW/4',follow_redirects=True)
    assert result.status == '200 OK'
    assert b"Jhonny" in resp.data
    assert b"Jhonny@yahoo.com" in resp.data


def test_add_two_users(client):
    """Test if a new post can be added"""
    sign_in_user(client, "admin@localhost.com", "1234")
    result =  add_user(client, "Jhon", "bldda@yahoo.com", "1234")
    add_user(client, "Peter", "peter@yahoo.com", "1234")
    resp1 = client.get('/USER/VIEW/5',follow_redirects=True)
    resp2 = client.get('/USER/VIEW/6',follow_redirects=True)
    assert result.status == '200 OK'
    assert b"Jhon" in resp1.data
    assert b'bldda@yahoo.com' in resp1.data
    assert b"Peter" in resp2.data
    assert b"peter@yahoo.com" in resp2.data

def test_view_user(client):
    """Test if a post can be viewed"""
    sign_in_user(client, "admin@localhost.com", "1234")
    add_user(client,"Blacky", "bla@gmail.com", "7213")
    result = view_user(client)
    assert b'Blacky' in result.data
    assert b'bla@gmail.com' in result.data


def test_update_user(client):
    """Test if a post can be updated"""
    sign_in_user(client, "admin@localhost.com", "1234")
    add_user(client,"Jhon", "Jhon@yahoo.com", "sdasd")
    result = update_user(client, "Jhon update","Jhon@yahoo.com", "21")
    assert result.status == '200 OK'
    assert b'Jhon update' in result.data
    assert b'Jhon@yahoo.com' in result.data


def test_delete_user(client):
    """Test if a post can be deleted"""
    sign_in_user(client, "admin@localhost.com", "1234")
    result = add_user(client,"Maggie", "new@yahoo.com", "67123")
    result = delete_user(client)
    response = client.get('/USER/' , follow_redirects=True)
    assert b'User deleted' in result.data
    assert b'Maggie' not in response.data
    assert b'new@yahoo.com' not in response.data

def test_redirect_not_setup(client):
    ContainerService.memory_config.set_configuration = False
    response = client.get("/USER/",follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Host" in response.data
    assert b"Database" in response.data
    assert b"User" in response.data
    assert b"Password" in response.data
    assert b"Read about true experiences," not in response.data
    response = client.get("/USER/",follow_redirects=True)
    assert b"Host" in response.data
    response = client.get("/USER/VIEW/1",follow_redirects=True)
    assert b"Host" in response.data
    response = client.get("/USER/UPDATE/1",follow_redirects=True)
    assert b"Host" in response.data
    response = client.get("/USER/DELETE/1",follow_redirects=True)
    assert b"Host" in response.data

def test_redirect_setup_true(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "admin@localhost.com", "1234")
    response = client.get('/USER/', follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Read about true experiences" in response.data
