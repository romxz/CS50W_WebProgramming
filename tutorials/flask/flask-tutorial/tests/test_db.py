import sqlite3

import pytest
from src.flaskr.db import get_db

def test_get_close_db(app):
    # Check unique db instance within app context
    with app.app_context():
        db = get_db()
        assert db is get_db()
    
    # Check db catches incorrect SQL commands
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    # Check db is closed after context 
    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """Use runner fixture to test flask cli 'init-db' command"""
    # Object used to record db.init_db function access
    class Recorder(object):
        called = False
    
    # Mocking function
    def fake_init_db():
        Recorder.called = True
    
    # Use monkeypatch to mock db.init_db function
    monkeypatch.setattr('src.flaskr.db.init_db', fake_init_db)

    # Now invoke 'init-db' command in cli
    result = runner.invoke(args=['init-db'])

    # Verify correct access and response
    assert 'Initialized' in result.output
    assert Recorder.called
