""" Graphql Sport Schema Module """
from graphene import (String, Boolean, Int, ID, InputObjectType,
                      Field, relay, Schema, Argument, Mutation, Interface,
                      Connection, Node)
from graphene_sqlalchemy import SQLAlchemyObjectType

from helpers.utils import (input_to_dictionary)
from app import (DB)
from app.database import (Sport as SportModel)
from .total_count import TotalCount
from app.filters import FilterConnectionField


class SportAttribute(Interface):
    """Sport Graphql Attributes"""
    description = String()
    active = Boolean()


class SportNode(SQLAlchemyObjectType):
    """Sport Graphql Node output"""
    class Meta:
        """Sport Graphql Node output"""
        model = SportModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class SportConnection(Connection):
    """Sport Graphql Query output"""
    class Meta:
        """Sport Graphql Query output"""
        node = SportNode
        interfaces = (TotalCount,)


class CreateSportInput(InputObjectType, SportAttribute):
    """Create Sport Input fields derived from SportAttribute"""

"""
mutation AddSport($sport: CreateSportInput!) {
  createSport(sportData: $sport) {
    sport {
      id
      active
    }
  }
}

{ 
  "sport": {
    "description": "Basketball",
    "active": true
  }
}
"""

class CreateSport(Mutation):
    """Sport Graphql Create mutation"""
    sport = Field(lambda: SportNode,
                  description="Sport created by this mutation.")

    class Arguments:
        """Sport Create Arguments"""
        sport_data = CreateSportInput(required=True)

    def mutate(self, info, sport_data=None):
        """Sport Graphql mutation"""
        data = input_to_dictionary(sport_data)

        sport = SportModel(**data)
        sport_db = DB.session.query(SportModel).filter_by(description=data['description']).first()
        if sport_db:
            print('need to update')
            sport_db = sport
        else:
            DB.session.add(sport)
        DB.session.commit()

        return CreateSport(sport=sport)


class UpdateSportInput(InputObjectType, SportAttribute):
    """Sport Graphql Update Input"""
    id = ID(required=True, description="Global Id of the Sport.")

'''
mutation UpdateSport($sport: UpdateSportInput!) {
  updateSport(sportData: $sport) {
    sport {
      id
      active
    }
  }
}

{ 
  "sport": {
    "description": "Basketball",
    "active": false,
    "id": "U3BvcnQ6MTM="
  }
}
'''


class UpdateSport(Mutation):
    """Sport Graphql Update mutation"""
    sport = Field(lambda: SportNode,
                  description="Sport updated by this mutation.")

    class Arguments:
        """Sport Graphql Update arguments"""
        sport_data = UpdateSportInput(required=True)

    def mutate(self, info, sport_data):
        """Sport Graphql Update mutation"""
        data = input_to_dictionary(sport_data)

        sport = DB.session.query(SportModel).filter_by(id=data['id'])
        sport.update(data)
        DB.session.commit()
        sport = DB.session.query(SportModel).filter_by(id=data['id']).first()

        return UpdateSport(sport=sport)
