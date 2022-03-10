import sys
import os
from pathlib import Path

myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
#pylint: disable=redefined-outer-name
from main import create_app
import pytest
from services.service import ContainerService

test_app = create_app(test_config=True)


@pytest.fixture(name='input_test')
def input_test():
    return test_app.test_client()


def test_redirect_not_setup_false(input_test):
    ContainerService.memory_config.set_configuration = False
    response = input_test.get("/setup/",follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Host" in response.data
    assert b"Database" in response.data
    assert b"User" in response.data
    assert b"Password" in response.data
    assert b"Read about true experiences," not in response.data
    assert b"There are no blog posts." not in response.data
    response = input_test.get("/POST/",follow_redirects=True)
    assert b"Host" in response.data
    response = input_test.get("/POST/VIEW/1",follow_redirects=True)
    assert b"Host" in response.data
    response = input_test.get("/POST/UPDATE/1",follow_redirects=True)
    assert b"Host" in response.data
    response = input_test.get("/POST/DELETE/1",follow_redirects=True)
    assert b"Host" in response.data

def test_redirect_setup_true(input_test):
    ContainerService.memory_config.set_configuration = True
    response = input_test.get('/POST/', follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Read about true experiences," in response.data