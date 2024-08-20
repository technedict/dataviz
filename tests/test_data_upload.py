import os
import tempfile
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

def test_file_upload(client):
    # Login the test user
    user = User(username='testuser', email='test@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()
    
    client.post('/login', data=dict(email='test@example.com', password='testpassword'))
    
    # Upload a valid file
    data = {
        'file': (open('tests/valid_test_file.csv', 'rb'), 'valid_test_file.csv')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert b'File successfully uploaded and validated!' in response.data
    
    # Upload an invalid file
    data = {
        'file': (open('tests/invalid_test_file.txt', 'rb'), 'invalid_test_file.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert b'Invalid file format or data issues.' in response.data
