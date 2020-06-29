from werkzeug.security import check_password_hash, generate_password_hash

def has_user(db, username):
    return db.execute(
        'SELECT id FROM users WHERE username = ?', (username,)
    ).fetchone() is not None

def insert_user(db, username, password):
    db.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()

def get_user(db, username, password):
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    if user is None:
        return None
    elif not check_password_hash(user['password'], password):
        return None
    else:
        return user

def get_user_from_id(db, user_id):
    return db.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()

def get_channels_all(db):
    return db.execute(
        'SELECT id, topic, created'
        ' FROM channels ORDER BY created DESC'
    ).fetchall()

def has_channel(db, topic):
    return db.execute(
        'SELECT * FROM channels WHERE topic = ?', (topic,)
    ).fetchone() is not None

def insert_channel(db, topic):
    db.execute('INSERT INTO channels (topic) VALUES (?)', (topic,))
    db.commit()