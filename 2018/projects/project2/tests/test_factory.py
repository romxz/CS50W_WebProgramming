#from src.flaskr import create_app
from flack import create_app

def test_config():
    """Check app configures TESTING modes appropriately"""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    """Sanity check: Tests basic client 'Hello, World!' functionality"""
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
