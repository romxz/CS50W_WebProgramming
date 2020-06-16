from typing import List

def get_isbn(db: 'Database', isbn: str):
    return db.execute('SELECT * FROM books WHERE isbn = :isbn;', {'isbn': isbn}).fetchall()

def get_title(db: 'Database', title: str):
    return db.execute('SELECT * FROM books WHERE title LIKE :title;', {'title': '%'+title+'%'}).fetchall()

def get_author(db: 'Database', author: str):
    return db.execute('SELECT * FROM books WHERE author LIKE :author;', {'author': '%'+author+'%'}).fetchall()

def get_books(db: 'Database', searchby: dict):
    """ Search by one or more of ('isbn', 'title', 'author'). Later two are patterns used in LIKE """
    # Build query
    conditions = []
    params = {}
    #if 'isbn' in searchby:
    #    conditions.append('isbn = :isbn')
    #    params['isbn'] = searchby['isbn']
    for q in ['isbn', 'title', 'author']:
        if q in searchby:
            conditions.append(f'{q} ILIKE :{q}')
            params[q] = '%'+searchby[q]+'%'
    conditions = ' AND '.join(conditions)
    if not conditions:
        return False, None
    return db.execute('SELECT * FROM books WHERE '+conditions+';', params).fetchall()
