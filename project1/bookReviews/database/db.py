#import os
#import sqlite3 ## Using postgres for now
import csv
import click
from flask import current_app, g
from flask.cli import with_appcontext

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(clear_db_command)
    app.cli.add_command(db_tables_exist_command)


def get_db():
    if 'db' not in g:
        engine = create_engine(current_app.config['DATABASE_URL'])
        g.db = scoped_session(sessionmaker(bind=engine))
        ## sqlite3 boilerplate:
        #g.db = sqlite3.connect(
        #    current_app.config['DATABASE_URL'],
        #    detect_types=sqlite3.PARSE_DECLTYPES
        #)
        #g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # Users database
    touch_db_table(db, tablename='users')
    # Books database
    if not touch_db_table(db, tablename='books'):
        insert_books(db)
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database (touch only).')

def clear_db():
    db = get_db()
    db.execute("DROP TABLE IF EXISTS :name;", {"name": 'users'})
    db.execute("DROP TABLE IF EXISTS :name;", {"name": 'books'})
    db.commit()

@click.command('clear-db')
@with_appcontext
def clear_db_command():
    clear_db()
    click.echo('Clearing the database.')

@click.command('db-tables-exist')
@with_appcontext
def db_tables_exist_command():
    db = get_db()
    click.echo(f'Existing tables: users[{table_exists(db, "users")}], books[{table_exists(db, "books")}]')

def touch_db_table(db, tablename, commit=False):
    """ Create table using tablename+'CreateTable.sql' if table doesnt exist; 
        Returns True if table created, False otherwise"""
    if not table_exists(db, tablename):
        with current_app.open_resource(tablename+'CreateTable.sql') as tablefile:
            #print(f"Creating {tablename} table")
            db.execute(tablefile.read())
        if commit:
            db.commit()
        return False
    else:
        return True

def table_exists(db, tablename):
    """ Performs database query to test whether table tablename exists. Returns True if it does """
    try:
        exists = db.execute(
            "SELECT EXISTS ("
            "SELECT FROM information_schema.tables "
            "WHERE table_schema = 'public' AND table_name = :name );",
            {'name': tablename}).fetchone()
        return exists[0]
    except:
        raise Exception(f'Exists table {tablename} error')

def insert_books(db, commit=False):
    with current_app.open_resource("books.csv") as f:
        reader = csv.reader(f)
        next(reader)  # head
        for isbn, title, author, year in reader:
            db.execute(
                "INSERT INTO books (isbn, title, author, year) "
                "VALUES (:isbn, :title, :author, :year)",
                {"isbn": isbn, "title": title, "author": author, "year" : int(year)})
            if commit:
                db.commit()
            #print(f"Added book ({isbn},{title},{author},{year}).")