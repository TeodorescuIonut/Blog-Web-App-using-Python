import sys
import os
from pathlib import Path

import pytest

from tests.test_users_blueprint import add_user
myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
#pylint: disable=redefined-outer-name
from main import create_app
from services.service import ContainerService
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
def sign_out_user(client):
    return client.get('/SIGNOUT/', follow_redirects=True)

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
    assert b'Jhon' in response.data
    assert b'Sign Out' in response.data

def test_wrong_user(input_test):
    ContainerService.memory_config.set_configuration = True
    response = sign_in_user(input_test, "blas@yahoo.com", "1234")
    assert b'Wrong password or user, please try again.' in response.data

def test_already_signed_in_user(input_test):
    ContainerService.memory_config.set_configuration = True
    response = sign_in_user(input_test, "bla@yahoo.com", "1234")
    response = sign_in_user(input_test, "bla@yahoo.com", "1234")
    assert b'You are already logged in.' in response.data


def test_sign_out_user(input_test):
    ContainerService.memory_config.set_configuration = True
    sign_in_user(input_test, "bla@yahoo.com", "1234")
    response = sign_out_user(input_test)
    assert b'You have been logged out' in response.data

def test_redirect_not_setup(input_test):
    ContainerService.memory_config.set_configuration = False
    response = input_test.get("/SIGNIN/",follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Host" in response.data
    assert b"Database" in response.data
    assert b"User" in response.data
    assert b"Password" in response.data
    assert b"Read about true experiences," not in response.data
    response = input_test.get("/SIGNOUT/",follow_redirects=True)
    assert b"Host" in response.data


def test_redirect_setup_true(input_test):
    ContainerService.memory_config.set_configuration = True
    response = input_test.get('/SIGNIN/', follow_redirects=True)
    assert response.status == '200 OK'
    assert b'Email' in response.data
    assert b'Password' in response.data