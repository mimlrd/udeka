## __init__.py
# -*- coding: utf-8 -*-


from flask import Flask
from flask_s3 import FlaskS3
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from eduka.config import config,Config
import boto3




db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
# s3 = FlaskS3()
# s3 = boto3.client(
#     's3',
#     aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY
# )

# s3 = boto3.resource(
#    "s3",
#    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
#    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
# )

# result = s3.get_bucket_policy(Bucket="first-rep-eduka")
# print(result)



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
    #ßs3.init_app(app=app)

    return app
