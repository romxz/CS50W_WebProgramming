from typing import List

def get_reviews(db: 'Database', isbn: str):
    """Search in database for reviews using isbn."""
    # Build query
    return db.execute(
        'SELECT u.username, r.rating, r.review '
        'FROM reviews r INNER JOIN users u '
        'ON r.uid = u.id '
        'WHERE r.isbn = :isbn;', {'isbn': isbn}).fetchall()

def upsert_review(db: 'Database', uid: int, isbn: str, rating: float, review: str):
    """Upsert (update or insert) review into database"""
    db.execute(
        'INSERT INTO reviews (uid, isbn, rating, review) '
        'VALUES (:uid, :isbn, :rating, :review) '
        'ON CONFLICT (uid, isbn) ' #ON CONSTRAINT (uid, isbn) 
        'DO UPDATE SET rating = :rating, review = :review;',
        {'uid': uid, 'isbn': isbn, 'rating': rating, 'review': review})
    db.commit()

def review_counts(db: 'Database', isbn: int):
    return db.execute(
        'SELECT COUNT(*) AS review_count, AVG(rating) AS average_score '
        'FROM reviews WHERE isbn = :isbn GROUP BY isbn;',
        {'isbn': isbn}).fetchone()

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