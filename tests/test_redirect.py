from pickle import TRUE
import sys
import os
from pathlib import Path

from flask import redirect





myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
#pylint: disable=redefined-outer-name
from main import create_app
from interfaces.db_config_interface import IDatabaseConfig
import pytest
from services.service import ContainerService

test_app = create_app(test_config=True)


@pytest.fixture(name='client')
def client():
    return test_app.test_client()


def test_redirect_not_setup_false(client):
    
    ContainerService.memory_config.set_configuration = False
    response = client.get("/setup/",follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Host" in response.data
    assert b"Database" in response.data
    assert b"User" in response.data
    assert b"Password" in response.data
    assert b"Read about true experiences," not in response.data
    assert b"There are no blog posts." not in response.data

def test_redirect_setup_true(client):
    ContainerService.memory_config.set_configuration = True
    response = client.get('/POST/', follow_redirects=True)
    assert response.status == '200 OK'
    assert b"Read about true experiences," in response.data
    assert b"There are no blog posts." in response.data