""" Graphql Schema Module """
from graphene import (ObjectType, String, Field, relay, Schema, Argument,
                      Mutation)
from graphene_sqlalchemy_filter import FilterableConnectionField

from .filters import (FilterConnectionField)
from .schemas.team import (TeamNode, TeamConnection, CreateTeam, UpdateTeam)
from .schemas.sport import (SportNode, SportConnection, CreateSport,
                            UpdateSport, DeleteSport)
from .schemas.referee import (RefereeNode, RefereeConnection, CreateReferee,
                              UpdateReferee)
from .schemas.coach import (CoachNode, CoachConnection, CreateCoach,
                            UpdateCoach)
from .schemas.player import (PlayerNode, PlayerConnection, CreatePlayer,
                             UpdatePlayer)
from .schemas.address import (resolve_city_states, resolve_address,
                              CityStateNode, AddressNode)


class Query(ObjectType):
    """Create Query object list"""
    node = relay.Node.Field()

    city_state = Field(
        CityStateNode,
        postalcode=String(required=True),
        resolver=resolve_city_states
    )

    address = Field(
        AddressNode,
        postalcode=Argument(String, required=True),
        address1=Argument(String, required=True),
        address2=Argument(String),
        city=Argument(String),
        state=Argument(String),
        resolver=resolve_address
    )

 #   address = relay.Node.Field(AddressNode)
 #   citystate = relay.Node.Field(CityStateNode)
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

    deleteSport = DeleteSport.Field()

SCHEMA = Schema(query=Query, mutation=Mutation)
