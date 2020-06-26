import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .database.db import get_db

## password hash/validation from .dbUser instead
#from werkzeug.security import check_password_hash, generate_password_hash
from .database import dbUser

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        valid, uid = dbUser.authenticate(db, username, password)

        if not valid:
            error = 'Incorrect username/password'

        if error is None:
            session.clear()
            session['user_id'] = uid
            session['user_name'] = username
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif dbUser.has_user(db, username):
            error = f'User {username} already registered. Choose different username.'
        
        if error is None:
            dbUser.insert_new_user(db, username, password)
            return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/signup.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        ## Once userinfo/other table has been instantiated:
        #g.user = get_db().execute('SELECT * FROM userinfo WHERE id = :id', {'id': user_id}).fetchone()
        g.user = {'user_id': user_id, 'user_name': session.get('user_name')}

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view