from typing import List
from .dbModels import Book

def get_isbn(db: 'Database', isbn: str) -> List[Book]:
    return list(map(Book, db.execute('SELECT * FROM books WHERE isbn = :isbn;', {'isbn': isbn}).fetchall()))

def get_title(db: 'Database', title: str) -> List[Book]:
    return list(map(Book, db.execute('SELECT * FROM books WHERE title LIKE :title;', {'title': '%'+title+'%'}).fetchall()))

def get_author(db: 'Database', author: str) -> List[Book]:
    return list(map(Book, db.execute('SELECT * FROM books WHERE author LIKE :author;', {'author': '%'+author+'%'}).fetchall()))

def get_books(db: 'Database', searchby: dict) -> List[Book]:
    """ Search by one or more of ('isbn', 'title', 'author'). Later two are patterns used in LIKE """
    # Build query
    conditions = []
    params = {}
    for q in ['isbn', 'title', 'author']:
        if q in searchby:
            conditions.append(f'{q} ILIKE :{q}')
            params[q] = '%'+searchby[q]+'%'
    conditions = ' AND '.join(conditions)
    if not conditions:
        return False, None
    return list(map(Book, db.execute('SELECT * FROM books WHERE '+conditions+';', params).fetchall()))

"""
CREATE TABLE books (
    isbn VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);
"""
"""
def _unpack_book(db_book):
    isbn, title, author, year = db_book
    return Book(isbn=isbn, title=title, author=author, year=year)
"""