import pytest
from src.flaskr.db import get_db


def test_index(client, auth):
    """Test login/logout response using valid credentials"""
    # Access index with GET before login
    response = client.get('/')
    # Check response contains correct login/register options
    assert b'Log In' in response.data
    assert b'Register' in response.data
    # As well as no option to log out
    assert b'Log Out' not in response.data

    # Login with valid credentials
    auth.login()
    response = client.get('/')
    # Check GET index response now contains logout option
    assert b'Log Out' in response.data
    # As well as no option to log in / register
    assert b'Log In' not in response.data
    assert b'Register' not in response.data
    # As well as previous post history
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    # As well as link to update post history
    assert b'href="/1/update"' in response.data

    # Check response is again correct after loging out
    auth.logout()
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data
    assert b'Log Out' not in response.data

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    """Check user redirected to login before create, update, and delete view access"""
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'

def test_author_required(app, client, auth):
    """Check update, delete view access only for author of the corresponding post"""
    # Change post of author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE posts SET author_id = 2 WHERE id = 1')
        db.commit()
    
    # Login with valid credentials
    auth.login()
    # Current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    """Check update, delete views for a post return not found if post doesnt exist"""
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    """Test create view available to logged-in users upon GET,
    and correct insertion of new post with valid data"""
    # Login with valid credentials
    auth.login()
    # Check rendered /create view upon GET
    assert client.get('/create').status_code == 200
    # Create a valid post via POST
    client.post('/create', data={'title': 'created', 'body': ''})

    # Check new post is in database
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM posts').fetchone()[0]
        assert count == 2

def test_update(client, auth, app):
    """Check update view available to logged-in users upon GET,
    with correct updating of post when owner of post"""
    # Login with valid credentials
    auth.login()
    # Check rendered /update view upon GET with valid post id
    assert client.get('/1/update').status_code == 200
    # Update a valid post via POST
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    # Check post has been updated in database
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM posts WHERE id = 1').fetchone()
        assert post['title'] == 'updated'

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    """Check authorized create, validate views only take valid POST data"""
    # Login with valid credentials
    auth.login()
    # Submit incomplete data
    response = client.post(path, data={'title': '', 'body': ''})
    # Check response rejects
    assert b'Title is required.' in response.data


## The delete view should redirect to the index URL and the post should no longer
## exist in the database
def test_delete(client, auth, app):
    """Check redirection to index URL upon valid post deletion request"""
    # Login with valid credentials
    auth.login()
    # Submit valid request for deletion
    response = client.post('/1/delete')
    # Check redirection to index
    assert response.headers['Location'] == 'http://localhost/'

    # Select deleted post no longer available
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM posts WHERE id = 1').fetchone()
        assert post is None
