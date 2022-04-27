import pytest
from main import create_app
from io import BytesIO
from PIL import Image

from services.service import ContainerService

testing_app = create_app(test_config=True)


@pytest.fixture(name="client")
def test_client():
    return testing_app.test_client()


def sign_in_user(client, email, password):
    return client.post('/SIGNIN/', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def test_user_no_posts(client):
    """Check an empty blog"""
    sign_in_user(client, "admin@localhost.com", "1234")
    response = client.get('/statistics/')
    assert response.status == '200 OK'
    assert b"Peters" in response.data
    assert b"5" in response.data
    assert b"admin" in response.data
    assert b"6" in response.data
    assert b"Jhon_update" in response.data
    assert b"9" in response.data
    assert b"April-2022" in response.data


def test_not_signed_admin(client):
    sign_in_user(client, "bla@yahoo.com", "1234")
    client.get('/statistics/', follow_redirects=True)
    response = client.get('/POST/', follow_redirects=True)
    assert b'You need to be an admin to access this feature!' in response.data


def test_redirect_not_setup(client):
    ContainerService.memory_config.set_configuration = False
    response = client.get("/SIGNIN/", follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Host" in response.data
    assert b"Database" in response.data
    assert b"User" in response.data
    assert b"Password" in response.data
    assert b"Read about true experiences," not in response.data
    response = client.get("/SIGNOUT/", follow_redirects=True)
    assert b"Host" in response.data


def test_redirect_setup_true(client):
    ContainerService.memory_config.set_configuration = True
    response = client.get('/SIGNIN/', follow_redirects=True)
    assert response.status == '200 OK'
    assert b'Email' in response.data
    assert b'Password' in response.data
