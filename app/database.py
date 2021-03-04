from datetime import date
import enum
from dateutil.relativedelta import relativedelta
from sqlalchemy import (Column, Integer, String, Boolean, Date, ForeignKey,
                        Table, Enum)
from sqlalchemy.orm import (relationship, with_polymorphic)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression
from app import db


class Gender(enum.Enum):
    other = 0
    male = 1
    female = 2
    undefined = 99


class Level(db.Model):
    __tablename__ = 'level'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    level = Column(Integer)
    active = Column(Boolean, default=True, server_default=expression.true())


class Team(db.Model):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    active = Column(Boolean,  default=True, server_default=expression.true())


class Sport(db.Model):
    __tablename__ = 'sport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    active = Column(Boolean,  default=True, server_default=expression.true())


class Person(db.Model):
    __tablename__ = "person"
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
    gender = Column(Enum(Gender))


class Referee(Person):
    __tablename__ = 'referee'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship(
        "Sport", 
        foreign_keys=[sport_id])
    grade = Column(String(10))
    grade_date = Column(Date)
    active = Column(Boolean, default=True)


    @hybrid_property
    def years_grade(self):
        if self.grade_date:
            return relativedelta(date.today(), self.grade_date).years
        return 0


class Coach(Person):
    __tablename__ = 'coach'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    grade = Column(String(10))
    active = Column(Boolean, default=True)
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship(
        "Sport", 
        foreign_keys=[sport_id])
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship(
        "Team",
        foreign_keys=[team_id])


class Player(Person):
    __tablename__ = 'player'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship(
        "Sport", 
        foreign_keys=[sport_id])
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship(
        "Team", 
        foreign_keys=[team_id])
    active = Column(Boolean, default=True)
    birth_date = Column(Date)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship(
        "Parent",
        foreign_keys=[parent_id])


    @hybrid_property
    def age(self):
        if self.birth_date:
            return relativedelta(date.today(), self.birth_date).years
        return 0


class Parent(Person):
    __tablename__ = 'parent'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    active = Column(Boolean, default=True)
