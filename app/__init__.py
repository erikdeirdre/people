from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(environ.get('CONFIG_SETTINGS', "config.DevelopmentConfig"))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
