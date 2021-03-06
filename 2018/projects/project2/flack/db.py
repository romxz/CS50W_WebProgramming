import os
import sqlite3  # If using sqlite
#import csv
import click
from flask import current_app, g, session
from flask.cli import with_appcontext

## If using postgres/sqlalchemy
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(fill_db_test)
    #app.cli.add_command(clear_db_command)
    #app.cli.add_command(db_tables_exist_command)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        """
        engine = create_engine(current_app.config['DATABASE_URL'])
        g.db = scoped_session(sessionmaker(bind=engine))
        """
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database')

@click.command('fill-db-test')
@with_appcontext
def fill_db_test():
    """Fills database with simple test data."""
    # Load test data to insert into tables for testing
    with open(os.path.join(os.path.dirname(__file__), 'database/test_data.sql'), 'rb') as f:
        _data_sql = f.read().decode('utf8')
        get_db().executescript(_data_sql)