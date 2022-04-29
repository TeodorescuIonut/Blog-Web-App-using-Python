import pytest
from main import create_app
from io import BytesIO
from PIL import Image

testing_app = create_app(test_config=True)


@pytest.fixture(name="client")
def test_client():
    return testing_app.test_client()


def sign_in_user(client, email, password):
    return client.post('/SIGNIN/', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def test_app(client):
    """Check an empty blog"""
    response = client.get('/POST/')
    assert response.status == '200 OK'


def create_test_image(image_name):
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = image_name
    file.seek(0)
    return file


def add_post(client, title, content, owner, owner_id, image_file=None):
    return client.post('/POST/CREATE/posts', data=dict(
        title=title,
        owner=owner,
        content=content,
        owner_id=owner_id,
        image=image_file
    ), follow_redirects=True, content_type='multipart/form-data')


def update_post(client, title, content, owner,owner_id, image_file=None):
    return client.post('/POST/UPDATE/24', data=dict(
        title=title,
        owner=owner,
        content=content,
        owner_id=owner_id,
        image=image_file
    ), follow_redirects=True)


def test_add_post_with_image(client):
    sign_in_user(client, "admin@localhost.com", "1234")
    image_file = create_test_image('image.png')
    result = add_post(client, "Hello world", "bla bla", "admin", 2, image_file)
    resp = client.get('/POST/VIEW/23', follow_redirects=True)
    assert result.status == '200 OK'
    assert b"Hello World" in resp.data
    assert b"bla bla" in resp.data
    assert b"iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAWElEQVR4nO3PAQnAMBDAwF" \
           b"/9O6jYzUShYdwpSJ49884PrNsBpxipMVJjpMZIjZEaIzVGaozUGKkxUmOkxkiNkRojNUZqjNQYqTFSY6TGSI2RGiM1RmqM1HyxXQH+FhWRUgAAAABJRU5ErkJggg==" in resp.data


def test_add_post_without_image(client):
    sign_in_user(client, "admin@localhost.com", "1234")
    response = add_post(client, "Post with image", "bla bla", "admin", 2)
    assert response.status_code == 200
    resp = client.get('/POST/VIEW/24', follow_redirects=True)
    assert b'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAQAAAD2e2DtAAAABGdBTUEAALGPC' \
           b'/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA' \
           b'/4ePzL8AAAAJcEhZcwAAAEgAAABIAEbJaz4AAAAHdElNRQfmAQMTHQjMyy1mAAAByElEQVR42u3YvUkDYBSG0c+fQtDCwg2cxDlc0C0cwMbKwsohLGwCLpAEIoGb+JwzwVs8cOGuBQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAbHcxPWCvr/UwPeEIntbb9ITdrqcH7HW3bqcnHMHV9IB9LqcHMEsAcQKIE0CcAOIEECeAOAHECSDutD+B2z2vj+kJO7yu++kJhzrHAD7X+/SEHTbTAw7nBMQJIE4AcQKIE0CcAOIEECeAOAHECSBOAHECiBNAnADiBBAngDgBxAkgTgBxAogTQJwA4gQQJ4A4AcQJIE4AcQKIE0CcAOIEECeAOAHECSBOAHECiBNAnADiBBAngDgBxAkgTgBxAogTQJwA4gQQJ4A4AcQJIE4AcQKIE0CcAOIEECeAOAHECSBOAHECiBNAnADiBBAngDgBxAkgTgBxAogTQJwA4gQQJ4A4AcQJIE4AcdfTA/7gcf1MT9jhanrA4c4xgJfpAf+JExAngDgBxAkgTgBxAogTQJwA4gQQd9qfwO91Mz3hCDbTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgL/4BaAVC1TqmQ1kAAAAJXRFWHRjcmVhdGUtZGF0ZQAyMDEzLTAxLTIxVDIyOjUwOjM1LTA2OjAwUmwhZQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0xMS0xOFQwNjowNDoxNCswMDowMAPJqTcAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMTAtMjNUMDU6MjI6MDErMDA6MDDaHWubAAAAJXRFWHRtb2RpZnktZGF0ZQAyMDEzLTAxLTIxVDIyOjUwOjM1LTA2OjAwDd1XUQAAAABJRU5ErkJggg==' in resp.data
    assert b'Post With Image' in resp.data


def test_update_post_image(client):
    sign_in_user(client, "admin@localhost.com", "1234")
    image_file = create_test_image('new_image.png')
    response = update_post(client, "Post with image update", "bla bla", "admin", 2, image_file)
    assert response.status_code == 200
    resp = client.get('/POST/VIEW/24', follow_redirects=True)
    assert b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAWElEQVR4nO3PAQnAMBDAwF' \
           b'/9O6jYzUShYdwpSJ49884PrNsBpxipMVJjpMZIjZEaIzVGaozUGKkxUmOkxkiNkRojNUZqjNQYqTFSY6TGSI2RGiM1RmqM1HyxXQH+FhWRUgAAAABJRU5ErkJggg==' in resp.data
