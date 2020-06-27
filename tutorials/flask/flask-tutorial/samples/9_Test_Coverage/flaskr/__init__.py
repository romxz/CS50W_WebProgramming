import os

from flask import Flask

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page to say hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # initialize db with app
    from . import db
    db.init_app(app)

    # Initialize authorization blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    # Initialize main app feature (i.e. blog here) blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    # Make 'index' (@ blog app) root route
    app.add_url_rule('/', endpoint='index')

    return app