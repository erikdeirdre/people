""" Graphql Player Schema Module """
from graphene import (String, Boolean, Int, ID, InputObjectType,
                      Field, relay, Schema, Argument, Mutation, Interface,
                      Connection, Node)
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.filters import FilterConnectionField

from helpers.utils import (input_to_dictionary)
from app import (DB)
from app.database import (Player as PlayerModel)
from .total_count import TotalCount


class PlayerNode(SQLAlchemyObjectType):
    """ Player Node """
    class Meta:
        """ Player Node """
        model = PlayerModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class PlayerConnection(Connection):
    """Player Graphql Query output"""
    class Meta:
        """Player Graphql Query output"""
        node = PlayerNode
        interfaces = (TotalCount,)


class PlayerAttribute:
    """Player Input Template """
    first_name = String()
    last_name = String()
    address1 = String()
    address2 = String()
    city = String()
    state = String()
    zip_code = String()
    telephone = String()
    email = String(required=True)
    gender = String()
    sport = String()
    active = Boolean()
    team = String()


class CreatePlayerInput(InputObjectType, PlayerAttribute):
    """Create Player Input fields derived from PlayerAttribute"""


class CreatePlayer(Mutation):
    """Create Player Graphql"""
    player = Field(lambda: PlayerNode,
                  description="Player created by this mutation.")

    class Arguments:
        """Arguments for Create Player"""
        player_data = CreatePlayerInput(required=True)

    def mutate(self, info, player_data=None):
        """Create Player Graphql"""
        data = input_to_dictionary(player_data)

        player = PlayerModel(**data)
        player_db = DB.session.query(PlayerModel).filter_by(
            description=data['description']).first()
        if player_db:
            print('need to update')
            player_db = player
        else:
            DB.session.add(player)
        DB.session.commit()

        return CreatePlayer(player=player)


class UpdatePlayerInput(InputObjectType, PlayerAttribute):
    """Update Player Input fields derived from PlayerAttribute"""
    id = ID(required=True, description="Global Id of the Player.")


class UpdatePlayer(Mutation):
    """Update Player Graphql"""
    player = Field(lambda: PlayerNode,
                   description="Player updated by this mutation.")

    class Arguments:
        """Arguments for Update Player"""
        player_data = UpdatePlayerInput(required=True)

    def mutate(self, info, player_data):
        """Update Player Graphql"""
        data = input_to_dictionary(player_data)

        player = DB.session.query(PlayerModel).filter_by(id=data['id']).first()
        player.update(data)
        DB.session.commit()
        player = DB.session.query(PlayerModel).filter_by(id=data['id']).first()

        return UpdatePlayer(player=player)
