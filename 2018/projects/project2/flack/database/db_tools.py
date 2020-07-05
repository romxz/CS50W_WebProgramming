from werkzeug.security import check_password_hash, generate_password_hash

######################################################### Users
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


######################################################### Channels
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

def get_channel_id(db, topic):
    result = db.execute(
        'SELECT id FROM channels WHERE topic = ?', (topic,)
    ).fetchone()
    if result is None:
        return None
    else:
        return result['id']

######################################################### Messages
def row_to_dict(row):
    ## Hacky solution to: "TypeError: Cannot pickle sqlite3.Row objects"...
    return {k: v for k, v in zip(row.keys(), row)}

def rows_as_dicts(messages):
    ## Hacky solution to: "TypeError: Cannot pickle sqlite3.Row objects"...
    return map(row_to_dict, messages)

def get_all_messages(db, topic, limit=100, as_dicts=False):
    channel_id = get_channel_id(db, topic)
    if channel_id is None:
        return []
    messages = db.execute(
        'SELECT * FROM messages WHERE channel_id = ?'
        ' ORDER BY created DESC LIMIT ?', (channel_id, limit)
    ).fetchall()
    ## Hacky solution to: "TypeError: Cannot pickle sqlite3.Row objects"...
    if as_dicts: return rows_as_dicts(messages)
    else: return messages

def insert_message(db, channel_id, author_id, body, created=None):
    if created is None:
        query = 'INSERT INTO messages (channel_id, author_id, body) VALUES (?, ?, ?)'
        params = (channel_id, author_id, body)
    else:
        query = 'INSERT INTO messages (channel_id, author_id, created, body) VALUES (?, ?, ?, ?)'
        params = (channel_id, author_id, created, body)
    db.execute(query, params)
    db.commit()

def get_message(db, channel_id, author_id, created=None, as_dict=False):
    if created is None:
        query = 'SELECT * FROM messages WHERE channel_id = ? AND author_id = ?'
        params = (channel_id, author_id)
    else:
        query = 'SELECT * FROM messages WHERE channel_id = ? AND author_id = ? AND created = ?'
        params = (channel_id, author_id, created)
    if as_dict: return row_to_dict(db.execute(query, params).fetchone())
    else: return db.execute(query, params).fetchone()

###############################################################
# """
# CREATE TABLE channels (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     topic TEXT NOT NULL UNIQUE,
#     created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
# );

# CREATE TABLE messages (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     channel_id INTEGER NOT NULL,
#     author_id INTEGER NOT NULL,
#     created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     body TEXT NOT NULL,
#     FOREIGN KEY (channel_id) REFERENCES channels (id),
#     FOREIGN KEY (author_id) REFERENCES users (id)
# );
# """