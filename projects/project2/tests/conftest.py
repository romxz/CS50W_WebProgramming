import os
import tempfile

import pytest
#import flack #create_app
from flack import create_app
from flack.db import get_db, init_db
#from src.flaskr.db import get_db, init_db

# Load test data to insert into tables for testing
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """Calls the factory and passes test_config to configure app and db
    for testing instead of using local dev configuration"""

    # Create and open temporary file, returning file object and path
    db_fd, db_path = tempfile.mkstemp()

    # Create app with test mode and db path overridden
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Initialize tables and test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    
    yield app

    # After test is over, close and remove temp file
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Fixture to testing client making requests to app
    without running the server"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Fixture to test CLI client to call commands registered
    with the app without running the server"""
    return app.test_cli_runner()


###################### Authentication
class AuthActions:
    """Quick methods for a test client to login/register/logout"""
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        """POST-request for login and returns the response"""
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def register(self, username='regis', password='regis'):
        """POST-request for registering and returns the response"""
        return self._client.post(
            '/auth/register',
            data={'username': username, 'password': password}
        )

    def logout(self):
        """GET-request for logout and returns the response"""
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """Fixture passing object with common login/register/logout
    authorization methods using the client fixture."""
    return AuthActions(client)
