""" Graphql Team Schema Module """
from graphene import (String, Boolean, Int, ID, InputObjectType,
                      Field, relay, Schema, Argument, Mutation, Interface,
                      Connection, Node)
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import (FilterableConnectionField)

from helpers.utils import (input_to_dictionary)
from app import (DB)
from app.database import (Team as TeamModel)
from .total_count import TotalCount
from app.filters import FilterConnectionField


class TeamNode(SQLAlchemyObjectType):
    """ Team Node """
    class Meta:
        """ Team Node """
        model = TeamModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class TeamConnection(Connection):
    """ Team Connection """
    class Meta:
        """ Team Connection """
        node = TeamNode
        interfaces = (TotalCount,)


class TeamAttribute(Interface):
    """Team fields output """
    description = String()
    active = Boolean()


class CreateTeamInput(InputObjectType, TeamAttribute):
    """Create Team Input fields derived from TeamAttribute"""


class CreateTeam(Mutation):
    """Create Team Graphql"""
    team = Field(lambda: TeamNode,
                 description="Team created by this mutation.")

    class Arguments:
        """Arguments for Create Team"""
        team_data = CreateTeamInput(required=True)

    def mutate(self, info, team_data=None):
        """Mutation method for Create Team"""
        data = input_to_dictionary(team_data)

        team = TeamModel(**data)
        team_db = DB.session.query(TeamModel).filter_by(
            description=data['description']).first()
        if team_db:
            print('need to update')
            team_db = team
        else:
            DB.session.add(team)
        DB.session.commit()

        return CreateTeam(team=team)


class UpdateTeamInput(InputObjectType, TeamAttribute):
    """Update Team Input fields derived from TeamAttribute"""
    id = ID(required=True, description="Global Id of the Team.")


class UpdateTeam(Mutation):
    """Update Team Graphql"""
    team = Field(lambda: TeamNode,
                 description="Team updated by this mutation.")

    class Arguments:
        """Arguments for Update Team"""
        team_data = UpdateTeamInput(required=True)

    def mutate(self, info, team_data):
        """Mutation method for Update Team"""
        data = input_to_dictionary(team_data)

        team = DB.session.query(TeamModel).filter_by(id=data['id'])
        team.update(data)
        DB.session.commit()
        team = DB.session.query(TeamModel).filter_by(id=data['id']).first()

        return UpdateTeam(team=team)
