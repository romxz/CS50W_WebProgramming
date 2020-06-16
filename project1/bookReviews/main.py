from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .database.db import get_db
from .database import dbBooks
from .auth import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('public/index.html')

@bp.route('/profile')
def profile():
    return 'Profile'

@bp.route('/book')
@login_required
def book():#isbn: str):
    db = get_db()
    #revs = db.execute(
    #    'SELECT'
    #)
    isbn = request.args.get('isbn')
    return f'Reviews:{isbn}'

@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        searchby = dict()
        
        isbn = request.form.get('isbn')
        if isbn:
            searchby['isbn'] = isbn

        title = request.form.get('title')
        if title:
            searchby['title'] = title

        author = request.form.get('author')
        if author:
            searchby['author'] = author

        db = get_db()
        
        error = None
        book_results = None
        if not searchby:
            error = "Please provide a valid isbn, title, or author to search by"
        else:
            book_results = dbBooks.get_books(db, searchby)
        
        if not book_results:
            error = "Couldn't find results matching query"
        
        flash(error)
        return render_template('public/search.html', book_results=book_results)
        
    return render_template('public/search.html')