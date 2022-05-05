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


def test_users_menu_option_signed_admin(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "admin@localhost.com", "1234")
    response = client.get('/USER/', follow_redirects=True)
    assert b'Users' in response.data
    assert b'bla@yahoo.com' in response.data
    assert b'admin' in response.data


def test_users_menu_option_signed_user(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "bla@yahoo.com", "1234")
    response = client.get('/USER/', follow_redirects=True)
    assert b'Users' not in response.data


def test_update_option_signed_admin(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "admin@localhost.com", "1234")
    response = client.get('/USER/VIEW/0', follow_redirects=True)
    assert b'Update' in response.data
    assert b'Delete' in response.data


def test_update_option_signed_user(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "bla@yahoo.com", "1234")
    response = client.get('/USER/VIEW/0', follow_redirects=True)
    assert b'Update' in response.data
    response = client.get('/USER/UPDATE/0', follow_redirects=True)
    assert b'Name' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_delete_option_signed_admin(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "admin@localhost.com", "1234")
    response = client.get('/USER/VIEW/0', follow_redirects=True)
    assert b'Delete' in response.data


def test_delete_option_signed_user(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "bla@yahoo.com", "1234")
    add_post(client, "My title", 'blblblbl', 'Jhon', 1)
    response = client.get('/USER/DELETE/0', follow_redirects=True)
    assert b'You need to be an admin to access this feature!' in response.data


def test_not_signed_user(client):
    ContainerService.memory_config.set_configuration = True
    response = client.get('/USER/DELETE/0', follow_redirects=True)
    response = client.get('/POST/', follow_redirects=True)
    assert b'You need to be an admin to access this feature!' in response.data
    response = client.get('/POST/CREATE/posts', follow_redirects=True)
    response = client.get('/POST/', follow_redirects=True)
    assert b'You need to sign in to access this feature!' in response.data
    response = client.get('/USER/UPDATE/0', follow_redirects=True)
    response = client.get('/POST/', follow_redirects=True)
    assert b'403 - Not allowed' in response.data


def test_signed_user_update_other_user(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "admin@localhost.com", "1234")
    add_user(client, "Jane", "jane@yahoo.com", "123")
    sign_out_user(client)
    sign_in_user(client, "bla@yahoo.com", "1234")
    response = client.get('/USER/UPDATE/1', follow_redirects=True)
    response = client.get('/POST/', follow_redirects=True)
    assert b'403 - Not allowed' in response.data


def test_signed_user_update_other_users_post(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "jane@yahoo.com", "123")
    response = client.get('/POST/UPDATE/0', follow_redirects=True)
    response = client.get('/POST/', follow_redirects=True)
    assert b'403 - Not allowed' in response.data


def test_signed_user_delete_other_users_post(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "jane@yahoo.com", "123")
    response = client.get('/POST/DELETE/0', follow_redirects=True)
    response = client.get('/POST/', follow_redirects=True)
    assert b'403 - Not allowed' in response.data


def test_signed_user_view_other_users_post(client):
    ContainerService.memory_config.set_configuration = True
    response = client.get('/POST/VIEW/0', follow_redirects=True)
    assert b'My Title' in response.data
    assert b'Update' not in response.data
