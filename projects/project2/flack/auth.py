import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flack.db import get_db
from flack.database import db_tools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db_tools.has_user(db, username):
            error = f'User {username} is already registered.'
        
        if error is None:
            db_tools.insert_user(db, username, password)
            return redirect(url_for('auth.login'))
        
        flash(error)
    
    return render_template('auth/register.html.jinja')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = db_tools.get_user(get_db(), username, password)
            if user is None:
                error = 'Incorrect username or password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('lobby.index'))
        
        flash(error)
    
    return render_template('auth/login.html.jinja')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_tools.get_user_from_id(get_db(), user_id)

@bp.route('/logout')
def logout():
    # TODO: Need to make this user-only. Currently: clears out all server-side info
    session.clear()
    return redirect(url_for('lobby.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
