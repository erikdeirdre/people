""" Graphql Filter Module """
from graphene_sqlalchemy_filter import (FilterableConnectionField, FilterSet)
from .database import (Sport as SportModel, Team as TeamModel,
                       Coach as CoachModel, Referee as RefereeModel)


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


class RefereeFilter(FilterSet):
    """Referee Graphql Filter"""
    class Meta:
        """Referee Graphql Query output"""
        model = RefereeModel
        fields = {
            'last_name': ['eq', 'ilike'],
            'first_name': ['eq', 'ilike'],
            'address1': ['eq', 'ilike'],
            'address2': ['eq', 'ilike'],
            'city': ['eq', 'ilike'],
            'state': ['eq', 'ilike'],
            'zip_code': ['eq', 'ilike'],
            'active': ['eq']
        }


class CoachFilter(FilterSet):
    """Coach Graphql Filter"""
    class Meta:
        """Coach Graphql Query output"""
        model = CoachModel
        fields = {
            'last_name': ['eq', 'ilike'],
            'first_name': ['eq', 'ilike'],
            'address1': ['eq', 'ilike'],
            'address2': ['eq', 'ilike'],
            'city': ['eq', 'ilike'],
            'state': ['eq', 'ilike'],
            'zip_code': ['eq', 'ilike'],
            'active': ['eq']
        }


class FilterConnectionField(FilterableConnectionField):
    """ Consolidate the filters"""
    filters = {
        TeamModel: TeamFilter(), SportModel: SportFilter(),
        RefereeModel: RefereeFilter(), CoachModel: CoachFilter()
    }