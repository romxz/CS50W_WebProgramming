import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    with open('./.skey') as f:
        app.config['SECRET_KEY'] = f.readline().strip()
    
    # Check for environment variable
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")
    else: app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

    db.init_app(app)

    # blueprint for auth routes in app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth routes of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app