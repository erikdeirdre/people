""" Main Module """
from os import environ
from sys import (exit, stdout)
from flask import Flask
from flask_sqlalchemy import (SQLAlchemy)
from flask_migrate import Migrate
from flask_cors import CORS
from flask_graphql import GraphQLView
import logging

logging.basicConfig(stream=stdout,
                    level=environ.get("LOG_LEVEL", logging.INFO))

logging.info('Starting ...')

APP = Flask(__name__)
CORS(APP)
APP.config.from_pyfile('settings.py')

DB = SQLAlchemy(APP)

MIGRATE = Migrate(APP, DB)


if environ.get('USPS_USERID') is None:
    logging.error("USPS_USERID isn't set ... exiting")
    exit(9)

from .schema import SCHEMA

@APP.route('/')
def health():
    return 'healthy'


APP.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=SCHEMA,
        graphiql=APP.config['GRAPHIQL'],
        get_context=lambda: {'session': DB.session}
    )
)