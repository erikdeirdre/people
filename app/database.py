from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import (Column, Integer, String, Boolean, Float, Date,
                        ForeignKey)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression

from app import db


class Sport(db.Model):
    __tablename__ = 'sport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    active = Column(Boolean,  default=True, server_default=expression.true())


class Person(db.Model):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    address1 = Column(String(100))
    address2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(10))
    telephone = Column(String(10))
    email = Column(String(100))
    gender = Column(String(10))
    birth_date = Column(Date)

    @hybrid_property
    def age(self):
        if self.birth_date:
            return relativedelta(date.today(), self.birth_date).years
        return 0


class Referee(Person):
    __tablename__ = 'referee'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    sport = Column(Integer, ForeignKey('sport.id'))
    grade = Column(String(10))
    active = Column(Boolean, default=True)


class Coach(Person):
    __tablename__ = 'coach'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    sport = Column(Integer, ForeignKey('sport.id'))
    grade = Column(String(10))
    active = Column(Boolean, default=True)
