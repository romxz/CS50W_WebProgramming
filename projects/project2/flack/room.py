from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from flask_socketio import SocketIO, emit
from werkzeug.exceptions import abort

from flack.auth import login_required
from flack.db import get_db
from flack.database import db_tools
from collections import deque

bp = Blueprint('rooms', __name__, url_prefix='/rooms')

@bp.route('/<string:topic>')
@login_required
def index(topic):
    db = get_db()
    # Check if topic exists
    if not db_tools.has_channel(db, topic):
        if len(topic) > 10:
            topic = topic[:10] + '...'
        abort(404, f"Channel for topic {topic} doesn't exist.")
    
    # session
    g.topic = topic
    
    return render_template('rooms/room.html.jinja', topic=topic, messages=get_messages(topic))

def get_messages(topic):
    # Grab room_topics dictionary if it exists, otherwise create it
    room_topics = session.get('topics')
    if room_topics is None:
        room_topics = dict()
        session['topics'] = room_topics
    
    # Get all messages for that topic
    message_limit = 10
    messages = room_topics.get(topic)
    if messages is None:
        messages = deque(maxlen=message_limit)
        room_topics[topic] = messages

    # Fetch from database if no messages in session
    if len(messages) == 0:
        messages.extend(db_tools.get_messages(get_db(), topic, limit=message_limit, as_dicts=True))
    
    return messages

@socketio.on("submit message")
@login_required
def submit_message(data):
    pass
    # TODO: start here. Note: read about Flask-SocketIO sessions
    # https://blog.miguelgrinberg.com/post/flask-socketio-and-the-user-session

# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         body = request.form['body']
#         error = None
#         db = get_db()

#         if not body:
#             error = 'Message body is required.'
#         elif len(body) > 180:
#             error = 'Each message length most be shorter than 180 characters.'
#         elif db_tools.has_channel(db, topic):
#             error = 'Channel already exists.'
        
#         if error is not None:
#             flash(error)
#         else:
#             db_tools.insert_channel(db, topic)
#             return redirect(url_for('lobby.index'))
    
#     return render_template('rooms/create.html.jinja')

"""
TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    body TEXT NOT NULL,

"""