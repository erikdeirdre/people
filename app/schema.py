""" Graphql Schema Module """
import xmltodict

from graphene import (ObjectType, String, InputObjectType,
                      Field, relay, Schema, Argument, Mutation, Interface,
                      Connection, Node)
from graphene_sqlalchemy import (SQLAlchemyObjectType,
                                 SQLAlchemyConnectionField)
from graphene_sqlalchemy_filter import (FilterableConnectionField, FilterSet)

from .database import (Sport as SportModel, Team as TeamModel,
                       Coach as CoachModel, Referee as RefereeModel)
from .filters import (FilterConnectionField)
from .schemas.team import (TeamNode, TeamConnection, CreateTeam, UpdateTeam)
from .schemas.sport import (SportNode, SportConnection, CreateSport,
                            UpdateSport)
from .schemas.referee import (RefereeNode, RefereeConnection, CreateReferee,
                              UpdateReferee)
from .schemas.coach import (CoachNode, CoachConnection, CreateCoach,
                            UpdateCoach)
from .schemas.player import (PlayerNode, PlayerConnection, CreatePlayer,
                             UpdatePlayer)
from .schemas.address import (CityState, Address, resolve_city_states,
                              resolve_address)


class Query(ObjectType):
    """Create Query object list"""
    node = relay.Node.Field()

    city_state = Field(
        CityState,
        postalcode=Argument(String, required=True),
        resolver = resolve_city_states
    )

    address = Field(
        Address,
        postalcode=Argument(String, required=True),
        address1=Argument(String, required=True),
        address2=Argument(String),
        city=Argument(String),
        state=Argument(String),
        resolver = resolve_address
    )

    sport = relay.Node.Field(SportNode)
    team = relay.Node.Field(TeamNode)
    referee = relay.Node.Field(RefereeNode)
    coach = relay.Node.Field(CoachNode)
    player = relay.Node.Field(PlayerNode)

    all_team = FilterableConnectionField(TeamConnection)
    all_sport = FilterConnectionField(SportConnection)
    all_referee = FilterConnectionField(RefereeConnection)
    all_coach = FilterConnectionField(CoachConnection)
    all_player = FilterConnectionField(PlayerConnection)


class Mutation(ObjectType):
    """Create Mutation object list"""
    createReferee = CreateReferee.Field()
    createCoach = CreateCoach.Field()
    createSport = CreateSport.Field()
    createTeam = CreateTeam.Field()
    createPlayer = CreatePlayer.Field()

    updateTeam = UpdateTeam.Field()
    UpdateReferee = UpdateReferee.Field()
    updateCoach = UpdateCoach.Field()
    updateSport = UpdateSport.Field()
    updatePlayer = UpdatePlayer.Field()

SCHEMA = Schema(query=Query, mutation=Mutation)
