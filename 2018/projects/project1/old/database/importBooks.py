import csv
import os

import dbConnect

db = dbConnect.getDatabase()

def main():
    # Check table books exists, if not, create it
    touch_books()
    insert_books()

def touch_books():
    with open('booksExist.sql') as f:
        books_exist = db.execute(f.read()).fetchall()
    for book in books_exist:
        if not book[0]: 
            with open('createBooks.sql') as g:
                sqlFile = g.read()
                print(sqlFile)
                db.execute(sqlFile)
                db.commit()

def insert_books():
    with open("books.csv") as f:
        reader = csv.reader(f)
        head = next(reader)
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn": isbn, "title": title, "author": author, "year" : int(year)})
            print(f"Added book ({isbn},{title},{author},{year}).")
        db.commit()

if __name__ == "__main__":
    main()
