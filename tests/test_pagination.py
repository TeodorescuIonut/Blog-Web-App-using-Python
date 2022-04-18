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


def add_user(client, name, email, password):
    return client.post('/USER/CREATE/users', data=dict(
        name=name,
        email=email,
        password=password
    ), follow_redirects=True)


def test_no_of_posts_below_limit(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "bla@yahoo.com", "1234")
    add_post(client, "blue", "bla bla bla", "Jhon", 12)
    add_post(client, "yellow", "bla bla bla", "Jhon", 12)
    response = client.get('/POST/', follow_redirects=True)
    assert b'Next' not in response.data
    assert b'Previous' not in response.data


def test_no_of_posts_more_than_limit(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "bla@yahoo.com", "1234")
    add_post(client, "red", "bla bla bla", "Jhon", 12)
    add_post(client, "green", "same", "Jhon", 12)
    response = client.get('/POST/', follow_redirects=True)
    assert b'Next' in response.data
    assert b'1' in response.data
    assert b'Previous' not in response.data


def test_posts_on_middle_page(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "bla@yahoo.com", "1234")
    add_post(client, "pink", "bla bla bla", "Jhon", 12)
    add_post(client, "blue", "same", "Jhon", 12)
    add_post(client, "red", "same", "Jhon", 12)
    add_post(client, "brown", "same", "Jhon", 12)
    response = client.get('/POST/?page=2&selected_owner_id=-1', follow_redirects=True)
    assert b'Green' in response.data
    assert b'Jhon' in response.data
    assert b'2' in response.data
    assert b'Next' in response.data
    assert b'Previous' in response.data


def test_posts_on_last_page(client):
    ContainerService.memory_config.set_configuration = True
    response = client.get('/POST/?page=3&selected_owner_id=-1', follow_redirects=True)
    assert b'Next' not in response.data
    assert b'3' in response.data
    assert b'Previous' in response.data
