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


class LevelType(enum.Enum):
    """ Level Type """
    UNDEFINED = 0
    REFEREE = 1
    COACH = 2
    PLAYER = 3


class Level(DB.Model):
    """Table to describe skill levels for referees, coaches, and players"""
    __tablename__ = 'level'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    referee_sports = relationship("RefereeSport", back_populates="level")
    coach_sports = relationship("CoachSport", back_populates="level")
    active = Column(Boolean, default=True, server_default=expression.true())
    level_type = Column(Enum(LevelType))


class Team(DB.Model):
    """ Table defining a team """
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    coaches = relationship("Coach",
                           secondary='coach_team',
                           back_populates="teams")
    players = relationship("Player",
                           secondary='player_team',
                           back_populates="teams")
    active = Column(Boolean, default=True, server_default=expression.true())


class Sport(DB.Model):
    """ Table defining sports """
    __tablename__ = 'sport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    referees = relationship("Referee",
                            secondary='referee_sport',
                            back_populates="sports")
    coaches = relationship("Coach",
                           secondary='coach_sport',
                           back_populates="sports")
    players = relationship("Player",
                           secondary='player_sport',
                           back_populates="sports")
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
    birth_date = Column(Date)
    table_type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': table_type
    }

    @hybrid_property
    def age(self):
        """ function to return a person's age """
        if self.birth_date:
            return relativedelta(date.today(), self.birth_date).years
        return 0


class Referee(Person):
    """ Table for listing referees and their unique columns """
    __tablename__ = 'referee'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    sports = relationship("Sport",
                          secondary='referee_sport',
                          back_populates="referees")
    parents = relationship("Parent",
                           secondary='referee_parent',
                           back_populates="referees")
    active = Column(Boolean, default=True, server_default=expression.true())

    __mapper_args__ = {
        'polymorphic_identity':'referee',
    }


class RefereeSport(DB.Model):
    """ Table for multiple referee / sport associations"""
    __tablename__ = 'referee_sport'
    referee_id = Column(Integer, ForeignKey('referee.id'),
                        primary_key=True)
    sport_id = Column(Integer, ForeignKey('sport.id'),
                      primary_key=True)
    active = Column(Boolean, default=True, server_default=expression.true())
    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship("Level", back_populates="referee_sports")
    level_date = Column(Date)
    sport_org_id = Column(String(50))

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
    active = Column(Boolean, default=True, server_default=expression.true())
    teams = relationship("Team",
                         secondary='coach_team',
                         back_populates="coaches")
    sports = relationship("Sport",
                          secondary='coach_sport',
                          back_populates="coaches")

    __mapper_args__ = {
        'polymorphic_identity':'coach',
    }


class CoachSport(DB.Model):
    """ Table for multiple coach / sport associations"""
    __tablename__ = 'coach_sport'
    coach_id = Column(Integer, ForeignKey('coach.id'),
                      primary_key=True)
    sport_id = Column(Integer, ForeignKey('sport.id'),
                      primary_key=True)
    active = Column(Boolean, default=True, server_default=expression.true())
    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship("Level", back_populates="coach_sports")
    level_date = Column(Date)
    sport_org_id = Column(String(50))

    @hybrid_property
    def years_level(self):
        """ function to return a years of experience at a grade """
        if self.level_date:
            return relativedelta(date.today(), self.level_date).years
        return 0


class CoachTeam(DB.Model):
    """ Table for multiple coach / team associations"""
    __tablename__ = 'coach_team'
    coach_id = Column(Integer, ForeignKey('coach.id'),
                      primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'),
                     primary_key=True)
    join_date = Column(Date)
    active = Column(Boolean, default=True, server_default=expression.true())

    @hybrid_property
    def years_active(self):
        """ function to return a years of experience at a grade """
        if self.join_date:
            return relativedelta(date.today(), self.join_date).years
        return 0


class Player(Person):
    """ Table for listing players and their unique columns """
    __tablename__ = 'player'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    teams = relationship("Team",
                         secondary='player_team',
                         back_populates="players")
    sports = relationship("Sport",
                          secondary='player_sport',
                          back_populates="players")
    parents = relationship("Parent",
                           secondary='player_parent',
                           back_populates="players")
    active = Column(Boolean, default=True, server_default=expression.true())

    __mapper_args__ = {
        'polymorphic_identity':'player',
    }


class PlayerSport(DB.Model):
    """ Table for multiple player / sport associations"""
    __tablename__ = 'player_sport'
    player_id = Column(Integer, ForeignKey('player.id'),
                       primary_key=True)
    sport_id = Column(Integer, ForeignKey('sport.id'),
                      primary_key=True)
    active = Column(Boolean, default=True, server_default=expression.true())


class PlayerTeam(DB.Model):
    """ Table for multiple player / team associations"""
    __tablename__ = 'player_team'
    player_id = Column(Integer, ForeignKey('player.id'),
                       primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'),
                     primary_key=True)
    active = Column(Boolean, default=True, server_default=expression.true())
    join_date = Column(Date)

    @hybrid_property
    def years_active(self):
        """ function to return a years of experience at a grade """
        if self.join_date:
            return relativedelta(date.today(), self.join_date).years
        return 0

class Parent(Person):
    """ Table for listing parents """
    __tablename__ = 'parent'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    players = relationship("Player",
                           secondary='player_parent',
                           back_populates="parents")
    referees = relationship("Referee",
                           secondary='referee_parent',
                           back_populates="parents")
    active = Column(Boolean, default=True, server_default=expression.true())

    __mapper_args__ = {
        'polymorphic_identity':'parent',
    }


class PlayerParent(DB.Model):
    """ Table for player / parent associations"""
    __tablename__ = 'player_parent'
    player_id = Column(Integer, ForeignKey('player.id'),
                       primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'),
                       primary_key=True)
    active = Column(Boolean, default=True, server_default=expression.true())


class RefereeParent(DB.Model):
    """ Table for referee / parent associations. Needed for referees less than 18 years old"""
    __tablename__ = 'referee_parent'
    referee_id = Column(Integer, ForeignKey('referee.id'),
                       primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'),
                       primary_key=True)
    active = Column(Boolean, default=True, server_default=expression.true())
