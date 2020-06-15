import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .database.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login')
def login():
    return 'Login'

@bp.route('/signup')
def signup():
    return 'Signup'

@bp.route('/logout')
def logout():
    return 'Logout'
