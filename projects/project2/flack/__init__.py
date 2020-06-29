import os

from flask import Flask

def create_app(test_config=None):
    # Create and config app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev2093823073049872039874',
        DATABASE=os.path.join(app.instance_path, 'flack.sqlite'),
    )

    if test_config is None:
        # load the instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Simple test page to say hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # Initialize db with app
    from . import db
    db.init_app(app)

    # Initialize authorization blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # Initialize main feature blueprint
    from . import main
    app.register_blueprint(main.bp)
    # Make 'index' (@ main) root route
    app.add_url_rule('/', endpoint='index')

    return app