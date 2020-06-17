from typing import List
from .dbModels import UserReview, DatabaseReview, ReviewStats


def get_reviews(db: 'Database', isbn: str) -> List[UserReview]:
    """Search in database for reviews using isbn."""
    # Build query
    return list(map(UserReview, db.execute(
        'SELECT u.username, r.rating, r.review '
        'FROM reviews r INNER JOIN users u '
        'ON r.uid = u.id '
        'WHERE r.isbn = :isbn;', {'isbn': isbn}).fetchall()))

def upsert_review(db: 'Database', dbReview: DatabaseReview) -> None:
    """Upsert (update or insert) review into database"""
    db.execute(
        'INSERT INTO reviews (uid, isbn, rating, review) '
        'VALUES (:uid, :isbn, :rating, :review) '
        'ON CONFLICT (uid, isbn) ' #ON CONSTRAINT (uid, isbn) 
        'DO UPDATE SET rating = :rating, review = :review;',
        dbReview)
    db.commit()

def review_counts(db: 'Database', isbn: int) -> ReviewStats:
    res = db.execute(
        'SELECT COUNT(*) AS review_count, AVG(rating) AS average_score '
        'FROM reviews WHERE isbn = :isbn GROUP BY isbn;',
        {'isbn': isbn}).fetchone()
    if res:
        return ReviewStats(res)
    else:
        return None

""" reviews
uid INTEGER REFERENCES users,
isbn VARCHAR REFERENCES books,
rating FLOAT(2) NOT NULL,
review VARCHAR NOT NULL,
PRIMARY KEY (uid, isbn)
"""
""" users
id SERIAL PRIMARY KEY,
username VARCHAR NOT NULL UNIQUE,
khash VARCHAR NOT NULL
"""
"""
def _unpack_Reviews(db_review):
    username, rating, review = db_review
    return UserReview(username=username, rating=rating, review=review)
"""