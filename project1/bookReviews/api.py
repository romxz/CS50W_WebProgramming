from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .database.db import get_db
from .database import dbBooks, dbReviews
import json

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/<string:isbn>')
def api_isbn(isbn):
    db = get_db()
    book = dbBooks.get_isbn(db, isbn)
    result = dict()
    if not book:
        return json.dumps(result)
    else:
        isbn, title, author, year = book[0]
        
        result['title'] = title
        result['author'] = author
        result['year'] = year
        result['isbn'] = isbn
        review_stats = dbReviews.review_counts(db, isbn)
        if review_stats:
            result['review_count'], result['average_score'] = review_stats
        else:
            result['review_count'] = 0
        return json.dumps(result)
