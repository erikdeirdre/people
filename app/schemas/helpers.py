""" Includes Row Count in Graphql Queries """
from graphene import (Interface, Int, Boolean, String, ID, ObjectType, Date,
                      InputObjectType)


class TotalCount(Interface):
    """ Return Row Count """
    total_count = Int()

    def resolve_total_count(self, info):
        """  Return Row Count """
        return self.length


class Levels(ObjectType):
    """ Sports Graphql Attributes"""
    id = ID()
    description = String()
    active = Boolean()


class Sports(ObjectType):
    """ Sports Graphql Attributes for Referees and Coaches"""
    id = ID()
    description = String()
    active = Boolean()
    level = String()
    level_date = Date()
    level_years = Int()


class SportsPlayers(ObjectType):
    """ Sports Graphql Attributes for Players"""
    id = ID()
    description = String()
    active = Boolean()


class Teams(ObjectType):
    """ Teams Graphql Attributes"""
    id = ID()
    description = String()
    active = Boolean()
    join_date = Date()
    join_years = Int()


class SportsAttribute:
    """Sport Attribute for Coach and Referees"""
    description = String()
    active = Boolean()
    level = String()
    level_date = Date()
    level_years = Int()


class CreateSportsInput(InputObjectType, SportsAttribute):
    """Create Sports Input fields derived from SportsAttribute"""
