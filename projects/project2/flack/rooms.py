import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from flask_socketio import emit
from werkzeug.exceptions import abort

from flack import socketio
from flack.auth import login_required
from flack.db import get_db

from flack.database import db_tools
from collections import deque

bp = Blueprint('rooms', __name__, url_prefix='/rooms')
MAX_MESSAGES_PER_ROOM = 10

class RoomMessages:
    """Stores and returns server-side messages a for valid topic"""

    def __init__(self):
        self.room_messages = dict()
    
    def get_messages(self, topic) -> ('messages', 'error'):
        # Retrieve from cache if available
        if topic in self.room_messages:
            return list(self.room_messages[topic]), None
        
        # Else retrieve from database if topic has been created
        db = get_db()
        if db_tools.has_channel(db, topic):
            self.room_messages[topic] = deque(maxlen=MAX_MESSAGES_PER_ROOM)
            self.room_messages[topic].extend(db_tools.get_all_messages(
                db, topic, limit=MAX_MESSAGES_PER_ROOM, as_dicts=True))
            return list(self.room_messages[topic]), None
        
        # Else return with error message
        if len(topic) > 10:
            # Shorten topic name for visibility
            topic = topic[:10] + '...'
        return None, f"Channel for topic {topic} doesn't exist."

    def insert_message(self, topic, message_db, message_public):
        # Insert message into database
        db_tools.insert_message(get_db(), **message_db)
        # Insert message into local cache
        if topic not in self.room_messages:
            self.room_messages[topic] = deque(maxlen=MAX_MESSAGES_PER_ROOM)
        self.room_messages[topic].appendleft(message_public)

room_messages = RoomMessages()


@bp.route('/topic/<string:topic>')
@login_required
def index(topic):
    db = get_db()
    # Check if topic exists
    mgs, error = room_messages.get_messages(topic)
    if error is not None:
        abort(404, error)
    
    # session
    session['topic'] = topic
    g.topic = topic
    
    return render_template('rooms/room.html.jinja', topic=topic)

@bp.route('/messages', methods=('POST',))
@login_required
def messages():
    # Check topic
    topic = request.form['topic']
    if topic is None:
        return jsonify({'success': False, 'errors': ['No topic']})
    
    # Get messages for that topic
    msgs, error = room_messages.get_messages(topic)
    if error is not None:
        return jsonify({'success': False, 'errors': [error]})
    
    return jsonify({'success': True, 'messages': msgs})


#@login_required
@socketio.on("submit message")
def submit_message(data):
    errors = []

    ### Parse incoming message
    data_db = {'channel_id': None, 'author_id': None, 'body': None, 'created': None}
    data_public = {'username': None, 'body': None, 'created': None}

    ## Message: Body
    if 'message' not in data:
        errors.append("Data contains no 'message' attribute.")
    elif not data['message']:
        errors.append("Empty data['message'].")
    else:
        data_db['body'] = data_public['body'] = data['message']
    
    ## Message: Author
    data_db['author_id'] = session.get('user_id')
    if data_db['author_id'] is None:
        errors.append('No author_id.')
    data_public['username'] = session.get('username')
    if data_public['username'] is None:
        errors.append('No username in session.')
    
    ## Message: Topic
    topic = session.get('topic')
    if topic is None:
        errors.append('No topic in session.')
    else:
        db = get_db()
        data_db['channel_id'] = db_tools.get_channel_id(db, topic)
        if data_db['channel_id'] is None:
            errors.append('No channel_id.')
    
    ## Message: Created
    data_db['created'] = datetime.datetime.now()
    data_public['created'] = data_db['created'].strftime('%Y-%m-%d')

    # Insert message into database
    if not errors:
        room_messages.insert_message(topic, data_db, data_public)
        # Emit message
        emit('announce message', {'success': True, 'message': data_public}, broadcast=True)
    else:
        emit('announce message', {'success': False, 'errors': errors})
