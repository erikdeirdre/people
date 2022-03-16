""" Main Module """
from flask import Flask
from flask_sqlalchemy import (SQLAlchemy)
from flask_migrate import Migrate
from flask_cors import CORS
from flask_graphql import GraphQLView

APP = Flask(__name__)
CORS(APP)
APP.config.from_pyfile('settings.py')

DB = SQLAlchemy(APP)

MIGRATE = Migrate(APP, DB)

PO_URL = APP.config['USPS_URL']
PO_USERID = APP.config['USPS_USERID']

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