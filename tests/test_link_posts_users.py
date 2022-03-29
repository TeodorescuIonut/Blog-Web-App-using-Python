import pytest
from main import create_app
from services.service import ContainerService
from tests.test_authentication_blueprint import sign_in_user, sign_out_user
from tests.test_post_blueprint_owner import add_post
from decorators.dependency_injection.injector_di import injector
from interfaces.post_repository_interface import IPostRepository

test_app = create_app(test_config=True)

@pytest.fixture(name='input_test')
def client():
    return test_app.test_client()

def delete_user(input_test):
    return input_test.post('/USER/DELETE/1', follow_redirects=True)
@injector
def delete_users_post(repo: IPostRepository):
    repo.delete_all_user_posts(1)


def test_delete_user_should_delete_all_his_posts(input_test):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(input_test, "jane@yahoo.com", "123")
    add_post(input_test,"blue","bla bla bla","Jane" ,12)
    add_post(input_test,"yellow","bla bla bla","Jane" ,12)
    add_post(input_test,"green","bla bla bla","Jane" ,12)
    sign_out_user(input_test)
    sign_in_user(input_test, "admin@localhost.com", "1234")
    delete_user(input_test)
    delete_users_post()
    response = input_test.get('/POST/',follow_redirects=True)
    assert b'Blue'not in response.data
    assert b'Yellow'not in response.data
    assert b'Green'not in response.data
