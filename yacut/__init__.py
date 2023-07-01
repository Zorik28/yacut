import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from . import api_views, error_handlers, views
