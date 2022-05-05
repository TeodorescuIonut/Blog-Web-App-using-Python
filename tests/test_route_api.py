import pytest
from tests.test_post_blueprint_owner import add_post
from main import create_app
from services.service import ContainerService

test_app = create_app(test_config=True)


@pytest.fixture(name='client')
def input_test():
    return test_app.test_client()


def sign_in_user(client, email, password):
    return client.post('/SIGNIN/', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def sign_out_user(client):
    return client.get('/SIGNOUT/', follow_redirects=True)

def test_client_api_route(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "admin@localhost.com", "1234")
    response = client.get('/POST/view/client-api/0', follow_redirects=True)
    assert b'get_info(0)' in response.data


def test_response_api_for_valid_post(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "admin@localhost.com", "1234")
    response = client.get('/api/post/0', follow_redirects=True)
    assert b'blblblbl' in response.data
    assert b'Jhon' in response.data
    assert b'My Title' in response.data


def test_response_api_for_nonvalid_post(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "admin@localhost.com", "1234")
    response = client.get('/api/post/55', follow_redirects=True)
    assert b'Post Not Found' in response.data


def test_redirect_not_setup(client):
    ContainerService.memory_config.set_configuration = False
    sign_out_user(client)
    response = client.get("/api/post/2", follow_redirects=True)
    assert b"Host" in response.data
    assert b"Database" in response.data
    assert b"User" in response.data
    assert b"Password" in response.data


def test_redirect_setup_true(client):
    ContainerService.memory_config.set_configuration = True
    response = client.get('/api/post/0', follow_redirects=True)
    assert response.status == '200 OK'
    assert b'blblblbl' in response.data
    assert b'Jhon' in response.data
    assert b'My Title' in response.data