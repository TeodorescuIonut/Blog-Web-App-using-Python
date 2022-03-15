import sys
import os
from pathlib import Path

import pytest
from services.service import ContainerService
from tests.test_users import add_user
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
#pylint: disable=redefined-outer-name
from main import create_app

test_app = create_app(test_config=True)


@pytest.fixture(name='input_test')
def input_test():
    return test_app.test_client()
def sign_in_user(client, email, password):
    return client.post('/SIGNIN/', data = dict(
         email = email,
         password = password
    )
    , follow_redirects=True)

def test_sign_in(input_test):
    ContainerService.memory_config.set_configuration = True
    response = input_test.get('/SIGNIN/',follow_redirects=True)
    assert response.status == '200 OK'
    assert b'Email' in response.data
    assert b'Password' in response.data
    
def test_existing_user(input_test):
    ContainerService.memory_config.set_configuration = True
    add_user(input_test, "Jhon", "bla@yahoo.com", "1234")
    sign_in_user(input_test, "bla@yahoo.com", "1234")
    response = input_test.get('/USER/',follow_redirects=True)
    assert b'Welcome back Jhon' in response.data

    