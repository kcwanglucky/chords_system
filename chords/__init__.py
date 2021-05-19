import os

from flask import Flask

from chords import auth, song_display
from chords.db_models import db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'chord.sqlite'),
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
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db.init_app(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()  # Create sql tables for our data models
        db.session.commit()

        app.register_blueprint(auth.bp)
        app.register_blueprint(song_display.bp)

        return app

    # app.register_blueprint(auth.bp)
    # app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')

    # return app
