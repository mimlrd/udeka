## __init__.py


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from eduka.config import config



db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    #with app.app_context():
    #    db.create_all()
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    return app
