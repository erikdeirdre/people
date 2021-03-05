""" Database Module """
from datetime import date
import enum
from dateutil.relativedelta import relativedelta
from sqlalchemy import (Column, Integer, String, Boolean, Date, ForeignKey,
                        Enum)
from sqlalchemy.orm import (relationship)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression
from app import DB


class Gender(enum.Enum):
    """Gender enum"""
    OTHER = 0
    MALE = 1
    FEMALE = 2
    UNDEFINED = 99


#class Level(DB.Model):
#    """Table to describe skill levels for referees, coaches, and players"""
#    __tablename__ = 'level'
#    id = Column(Integer, primary_key=True, autoincrement=True)
#    description = Column(String(100))
#    level = Column(Integer)
#    active = Column(Boolean, default=True, server_default=expression.true())


class Team(DB.Model):
    """ Table defining a team """
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    active = Column(Boolean, default=True, server_default=expression.true())


class Sport(DB.Model):
    """ Table defining sports """
    __tablename__ = 'sport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    active = Column(Boolean,  default=True, server_default=expression.true())


class Person(DB.Model):
    """ Base table for players, coaches, referees, and parents """
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
    """ Table for listing referees and their unique columns """
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
        """ function to return a years of experience at a grade """
        if self.grade_date:
            return relativedelta(date.today(), self.grade_date).years
        return 0


class Coach(Person):
    """ Table for listing coaches and their unique columns """
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
    """ Table for listing players and their unique columns """
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
        """ function to return a player's age """
        if self.birth_date:
            return relativedelta(date.today(), self.birth_date).years
        return 0


class Parent(Person):
    """ Table for listing parents """
    __tablename__ = 'parent'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    active = Column(Boolean, default=True)
