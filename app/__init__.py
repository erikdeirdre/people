""" Main Module """
from os import environ

from flask import Flask
from sqlalchemy import (Column, Integer, ForeignKey)
from flask_sqlalchemy import (SQLAlchemy, Model)
from sqlalchemy.ext.declarative import declared_attr
from flask_migrate import Migrate
from flask_cors import CORS


APP = Flask(__name__)
CORS(APP)
APP.config.from_object(environ.get('CONFIG_SETTINGS', "config.DevelopmentConfig"))

DB = SQLAlchemy(APP)

MIGRATE = Migrate(APP, DB)

PO_URL = APP.config['POST_OFFICE_URL']
PO_USERID = APP.config['POST_OFFICE_USERID']

from app import routes
