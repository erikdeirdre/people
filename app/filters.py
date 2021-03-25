""" Graphql Filter Module """
from graphene_sqlalchemy_filter import (FilterableConnectionField, FilterSet)
from .database import (Sport as SportModel, Team as TeamModel,
                       Person as PersonModel, Coach as CoachModel,
                       Referee as RefereeModel)


class TeamFilter(FilterSet):
    """Team Graphql Filter"""
    class Meta:
        """Team Graphql Filter output"""
        model = TeamModel
        fields = {
            'description': ['eq', 'ilike'],
            'active': ['eq']
        }


class SportFilter(FilterSet):
    """Sport Graphql Filter"""
    class Meta:
        """Sport Graphql Query output"""
        model = SportModel
        fields = {
            'description': ['eq', 'ilike'],
            'active': ['eq']
        }        


class FilterConnectionField(FilterableConnectionField):
    filters = {TeamModel: TeamFilter(), SportModel: SportFilter()}