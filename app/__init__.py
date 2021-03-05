""" Main Module """
from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


APP = Flask(__name__)
APP.config.from_object(environ.get('CONFIG_SETTINGS', "config.DevelopmentConfig"))
DB = SQLAlchemy(APP)
migrate = Migrate(APP, DB)

PO_URL = APP.config['POST_OFFICE_URL']
PO_USERID = APP.config['POST_OFFICE_USERID']

CORS(APP)

from app import routes
