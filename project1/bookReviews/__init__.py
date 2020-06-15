import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in models
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)  # instance_relative_config=True

    # Use test_config if provided, else build from local/
    if test_config is None:
        # Add secret key to app
        if not os.path.isfile('bookReviews/local/.skey'):
            msg = f'Please provide a key in "local/.skey"; {os.path.abspath(".")=}'
            #print(msg)
            raise Exception(msg)
        else:
            try:
                with open('bookReviews/local/.skey') as f:
                    app.config['SECRET_KEY'] = f.readline().strip()
            except:
                raise Exception('Please provide a key in "/local/.skey"')
        
        # Check for database environment variable
        if not os.getenv("DATABASE_URL"): 
            raise RuntimeError("DATABASE_URL is not set")
        else: 
            app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    else:
        app.config.from_mapping(test_config)

    # Check instance folder exists
    try:
        pass #os.makedirs(app.instance_path)
    except OSError:
        pass
    
    '''
    # Initialize SQLAlchemy with flask app
    db.init_app(app)

    # blueprint for auth routes in app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth routes of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    '''

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    return app