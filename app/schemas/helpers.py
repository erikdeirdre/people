""" Includes Row Count in Graphql Queries """
from graphene import (Interface, Int, Boolean, String, ID, ObjectType, Date)


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
    """ Sports Graphql Attributes"""
    id = ID()
    description = String()
    active = Boolean()
    achieve = String()
    achieve_date = Date()
    achieve_years = Int()


class Teams(ObjectType):
    """ Teams Graphql Attributes"""
    id = ID()
    description = String()
    active = Boolean()
    join_date = Date()
    join_years = Int()