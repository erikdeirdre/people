""" Database Module """
from datetime import date
import enum
from dateutil.relativedelta import relativedelta
from sqlalchemy import (Column, Integer, String, Boolean, Date, ForeignKey,
                        Enum)
from sqlalchemy.orm import relationship
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
    referees = relationship("Referee", back_populates="level")
    coaches = relationship("Coach", back_populates="level")
    active = Column(Boolean, default=True, server_default=expression.true())


class Team(DB.Model):
    """ Table defining a team """
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    coaches = relationship("Coach", back_populates="team")
    players = relationship("Player", back_populates="team")
    active = Column(Boolean, default=True, server_default=expression.true())


class Sport(DB.Model):
    """ Table defining sports """
    __tablename__ = 'sport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    referees = relationship("Referee", back_populates="sport")
    coaches = relationship("Coach", back_populates="sport")
    players = relationship("Player", back_populates="sport")
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
    table_type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': table_type
    }


class Referee(Person):
    """ Table for listing referees and their unique columns """
    __tablename__ = 'referee'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship("Sport", back_populates="referees")
    active = Column(Boolean)
    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship("Level", back_populates="referees")
    level_date = Column(Date)

    __mapper_args__ = {
        'polymorphic_identity':'referee',
    }

    @hybrid_property
    def years_level(self):
        """ function to return a years of experience at a grade """
        if self.level_date:
            return relativedelta(date.today(), self.level_date).years
        return 0


class Coach(Person):
    """ Table for listing coaches and their unique columns """
    __tablename__ = 'coach'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    active = Column(Boolean)
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship("Team", back_populates="coaches")
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship("Sport", back_populates="coaches")
    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship("Level", back_populates="coaches")
    level_date = Column(Date)

    __mapper_args__ = {
        'polymorphic_identity':'coach',
    }

    @hybrid_property
    def years_level(self):
        """ function to return a years of experience at a grade """
        if self.level_date:
            return relativedelta(date.today(), self.level_date).years
        return 0


class Player(Person):
    """ Table for listing players and their unique columns """
    __tablename__ = 'player'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship("Team", back_populates="players")
    birth_date = Column(Date)
 #   parent_id = Column(Integer, ForeignKey('parent.id'))
 #   parent = relationship("Parent", back_populates="players")
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship("Sport", back_populates="players")
    active = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity':'player',
    }

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
    __mapper_args__ = {
        'polymorphic_identity':'parent',
    }

    active = Column(Boolean)
