from os import environ

from flask import Flask
from sqlalchemy import (Column, Integer, ForeignKey)
from flask_sqlalchemy import (SQLAlchemy, Model)
from sqlalchemy.ext.declarative import declared_attr
from app.database import (Coach)


APP = Flask(__name__)
APP.config.from_object(environ.get('CONFIG_SETTINGS', "config.DevelopmentConfig"))

DB = SQLAlchemy(APP)

c = Coach(
  last_name="White",
  first_name="Peter"
)

DB.session.add(c)

DB.session.commit()