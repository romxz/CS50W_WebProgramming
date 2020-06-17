from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .database.db import get_db
from .database import dbBooks, dbReviews, goodReads
from .auth import login_required
from .database.dbModels import UserReview, DatabaseReview, ReviewStats, Book
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('public/index.html')

@bp.route('/profile')
def profile():
    return 'Profile'

@bp.route('/book', methods=('GET', 'POST'))
@login_required
def book():#isbn: str):
    """Serves book info and its reviews"""
    db = get_db()
    if request.method == "POST":
        #g.user = {'user_id': user_id, 'user_name}
        errors = []
        uid = request.form.get('book-submit-review-user-id')
        if uid is None:
            errors.append('uid is None')
        else:
            uid = int(uid)
        
        isbn = request.form.get('book-submit-review-book-isbn')
        if isbn is None:
            errors.append('isbn is None')
        
        rating = request.form.get('book-submit-review-rating')
        if rating is None:
            errors.append('rating is None')
        else: 
            rating = float(rating)
        
        review = request.form.get('book-submit-review-textarea')
        if review is None:
            errors.append('review is None')
        
        if not errors:
            dbReviews.upsert_review(db, DatabaseReview(uid=uid, isbn=isbn, rating=rating, review=review))
            return redirect(url_for('main.book', isbn=isbn))
        else:
            return 'Errors: ' + '; '.join(e for e in errors)
    else:    
        isbn = request.args.get('isbn')
        errors = dict()
        
        # fetch book by ISBN
        book = dict()
        try:
            book = dbBooks.get_isbn(db, isbn)[0]
        except Exception as e:
            errors['isbn'] = e
        
        # fetch Reviews by ISBN
        try:
            reviews = dbReviews.get_reviews(db, isbn)
        except Exception as e:
            errors['reviews'] = e
        
        # fetch GoodReads using API
        try:
            counts = goodReads.review_counts(isbn)
        except Exception as e:
            errors['goodReads'] = e
        
        if not errors:
            return render_template('user/book.html', book=book, reviews=reviews, counts=counts)
        else:
            return 'Errors: ' + '; '.join((f'{k}:{e}' for k,e in errors.items()))
        
        #return f'Error={error}; tb={e}'

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