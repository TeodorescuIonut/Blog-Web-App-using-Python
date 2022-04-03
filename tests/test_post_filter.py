import pytest
from tests.test_authentication_blueprint import sign_in_user
from tests.test_authorization import add_user
from main import create_app
from services.service import ContainerService
test_app = create_app(test_config=True)

@pytest.fixture(name='client')
def input_test():
    return test_app.test_client()

def test_filter_by_user_with_posts(client):
    ContainerService.memory_config.set_configuration = True
    response = client.get('/POST/?selected_owner_id=0',follow_redirects=True)
    assert b'Jhon_update' in response.data
    assert b'Next'  in response.data
    response = client.get('/POST/?page=2&selected_owner_id=0',follow_redirects=True)
    assert b'Jhon_update' in response.data
    assert b'Previous'  in response.data
    assert b'Next' not in response.data
    assert b'Hello world update' in response.data

def test_filter_by_user_without_posts(client):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(client, "admin@localhost.com", "1234")
    add_user(client, "Paul", "paul@yahoo.com", "1234")
    response = client.get('/POST/?selected_owner_id=3',follow_redirects=True)
    assert b'There are no blog posts.' in response.data
    assert b'Paul' in response.data
    assert b'Previous' not in response.data
    assert b'Next' not in response.data

def test_filter_by_all_users(client):
    ContainerService.memory_config.set_configuration = True
    response = client.get('/POST/?selected_owner_id=-1',follow_redirects=True)
    assert b'Next'  in response.data
    response = client.get('/POST/?page=2&selected_owner_id=-1',follow_redirects=True)
    assert b'Previous'  in response.data
    assert b'2'  in response.data
    assert b'Next'  in response.data
    response = client.get('/POST/?page=3&selected_owner_id=-1',follow_redirects=True)
    assert b'Previous'  in response.data
    assert b'3'  in response.data
    assert b'Next'  in response.data
    response = client.get('/POST/?page=4&selected_owner_id=-1',follow_redirects=True)
    assert b'Previous'  in response.data
    assert b'4'  in response.data
    assert b'Next'  in response.data
    response = client.get('/POST/?page=5&selected_owner_id=-1',follow_redirects=True)
    assert b'Previous'  in response.data
    assert b'5'  in response.data
    assert b'Next' not in response.data