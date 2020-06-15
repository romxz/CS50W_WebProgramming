from flask import Blueprint
from .database.db import get_db

#main = Blueprint('main', __name__)
bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/')
def root():
    return 'Index'

@bp.route('/index')
def index():
    return 'Index'

@bp.route('/profile')
def profile():
    return 'Profile'

@bp.route('/reviews')
def reviews():
    return 'Reviews'