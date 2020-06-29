from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flack.auth import login_required
from flack.db import get_db
from flack.database import db_tools

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    channels = db_tools.get_channels_all(get_db())
    return render_template('channels/index.html.jinja', channels=channels)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        topic = request.form['topic']
        error = None
        db = get_db()

        if not topic:
            error = 'Topic is required.'
        elif len(topic) > 24:
            error = 'Topic length most be shorter than 25 characters.'
        elif db_tools.has_channel(db, topic):
            error = 'Channel already exists.'
        
        if error is not None:
            flash(error)
        else:
            db_tools.insert_channel(db, topic)
            return redirect(url_for('main.index'))
    
    return render_template('channels/create.html.jinja')