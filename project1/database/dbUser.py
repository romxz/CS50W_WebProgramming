import hashlib, binascii
import os


def get_new_credentials(username: str, password: str) -> str:
    return _make_hash(password, binascii.b2a_hex(os.urandom(32)).decode())

def _get_db_hash(db: 'Database', username: str):
    creds = db.execute(
        "SELECT khash FROM users WHERE username = :username", 
        {"username": username}).fetchone()
    return creds

def has_user(db: 'Database', username: str):
    return _get_db_hash(db, username) is not None

def authenticate(db: 'Database', username: str, password: str):
    try:
        khash, = _get_db_hash(db, username)
        return khash == _make_hash(password, khash[:64])
    except:
        return False

def insert_user(db: 'Database', username: str, khash: str, commit=True):
    db.execute(
        "INSERT INTO users (username, khash) VALUES (:username, :khash);",
        {"username": username, "khash": khash})
    if commit: db.commit()

def delete_user(db: 'Database', username: str, commit=True):
    db.execute(
        "DELETE FROM users WHERE username = :username;",
        {"username": username})
    if commit: db.commit()

def _make_hash(password: str, salt: str) -> str:
    return salt+binascii.b2a_hex(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), binascii.a2b_hex(salt), 100_000)).decode()

#def main():
#    pass

#if __name__ == "__main__":
#    main()