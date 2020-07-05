import pytest
from flask import g, session
#from src.flaskr.db import get_db
from flack.db import get_db

###################### Register
def test_register(client, app):
    """Test register view access and successful new user registration in db"""
    # Should render successfully on GET
    assert client.get('/auth/register').status_code == 200

    # POST with valid data
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    # Should be redirectted to login URL
    assert response.headers['Location'] == 'http://localhost/auth/login'

    # New user should be on database
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM users WHERE username = 'a'",
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    """Test register message responses using incorrect username/password POST requests"""
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


###################### Login
def test_login(client, auth):
    """Test login view access and correct user login"""
    # Should render successfully on GET
    assert client.get('/auth/login').status_code == 200

    # POST login with valid credentials
    response = auth.login()
    # Should be redirected to index
    assert response.headers['Location'] == 'http://localhost/'

    # Correct user info should be available on session and g
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username or password.'),
    ('test', 'a', b'Incorrect username or password.'),
))
def test_login_validate_input(auth, username, password, message):
    """Test login message responses using incorrect username/password POST requests"""
    response = auth.login(username, password)
    assert message in response.data


###################### Logout
def test_logout(client, auth):
    """Test logout after successful login"""
    # Log in the user with correct credentials
    auth.login()

    # Check user_id no longer in session after logout
    with client:
        auth.logout()
        assert 'user_id' not in session
