from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(environ.get('CONFIG_SETTINGS', "config.DevelopmentConfig"))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

post_office_url = app.config["POST_OFFICE_URL"]
post_office_userid = app.config["POST_OFFICE_USERID"]

CORS(app)

from app import routes
