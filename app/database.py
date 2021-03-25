""" Database Module """
from datetime import (datetime, date)
import enum
from dateutil.relativedelta import relativedelta
from sqlalchemy import (Column, Integer, String, Boolean, Date, ForeignKey,
                        Enum, DateTime as DT)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr 
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression
from app import DB


class Gender(enum.Enum):
    """Gender enum"""
    OTHER = 0
    MALE = 1
    FEMALE = 2
    UNDEFINED = 99


class Level(DB.Model):
    """Table to describe skill levels for referees, coaches, and players"""
    __tablename__ = 'level'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    level = Column(Integer)
    active = Column(Boolean, default=True, server_default=expression.true())


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
    active = Column(Boolean, default=True, server_default=expression.true())


class Person(DB.Model):
    """ Base table for players, coaches, referees, and parents """
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    address1 = Column(String(100))
    address2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(15))
    telephone = Column(String(15))
    email = Column(String(100))
    gender = Column(Enum(Gender))


class Referee(DB.Model):
    """ Table for listing referees and their unique columns """
    __tablename__ = 'referee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship("Person", backref='referee')
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship("Sport", backref='sports')
    active = Column(Boolean)
    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship("Level", backref='levels')
    level_date = Column(Date)

    @hybrid_property
    def years_grade(self):
        """ function to return a years of experience at a grade """
        if self.grade_date:
            return relativedelta(date.today(), self.grade_date).years
        return 0


class Coach(DB.Model):
    """ Table for listing coaches and their unique columns """
    __tablename__ = 'coach'
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship("Person", backref='coach')
    active = Column(Boolean)
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship("Team", foreign_keys=[team_id])
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship("Sport", foreign_keys=[sport_id])

    #grade = relationship("Grade", foreign_keys=[grade.id])


class Player(DB.Model):
    """ Table for listing players and their unique columns """
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship("Person", backref='player')
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship("Team", foreign_keys=[team_id])
    birth_date = Column(Date)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", foreign_keys=[parent_id])
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship("Sport", foreign_keys=[sport_id])
    active = Column(Boolean)

    @hybrid_property
    def age(self):
        """ function to return a player's age """
        if self.birth_date:
            return relativedelta(date.today(), self.birth_date).years
        return 0


class Parent(DB.Model):
    """ Table for listing parents """
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship("Person", backref='parent')
    active = Column(Boolean)
