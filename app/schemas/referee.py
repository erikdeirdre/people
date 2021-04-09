""" Graphql Referee Schema Module """
from graphene import (String, Boolean, ID, InputObjectType, Field,
                      Mutation, Connection, Node, List, ObjectType)
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.filters import FilterConnectionField

from helpers.utils import (input_to_dictionary)
from app import (DB)
from app.database import (Referee as RefereeModel, Sport, RefereeSport)
from .helpers import (TotalCount, Sports)

class RefereeAttribute:
    """Referee Graphql Attributes"""
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
    grade = String()
    active = Boolean()


class RefereeNode(SQLAlchemyObjectType):
    """Referee Node """
    class Meta:
        """ Referee Node """
        model = RefereeModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory

    sport = List(Sports)

    def resolve_sport(self, info):
        ''' sport resolver '''
        sports = []
        results = DB.session.query(RefereeSport, Sport).join(Sport).filter(
            RefereeSport.referee_id == self.id)
        for row in results:
            achieve = None
            achieve_date = None
            achieve_years = 0
            description = None
            active = False
            if row.RefereeSport.level:
                achieve = row.RefereeSport.level.description
                achieve_date = row.RefereeSport.level_date
                achieve_years = row.RefereeSport.years_level
                description = row.Sport.description
                active = row.RefereeSport.active

            sports.append({'id': row.Sport.id,
                           'description': description,
                           'active': active,
                           'achieve': achieve,
                           'achieve_date': achieve_date,
                           'achieve_years': achieve_years})
        return sports


class RefereeConnection(Connection):
    """ Referee Connection """
    class Meta:
        """ Referee Connection """
        node = RefereeNode
        interfaces = (TotalCount,)


class CreateRefereeInput(InputObjectType, RefereeAttribute):
    """Create Referee Input fields derived from RefereeAttribute"""


class CreateReferee(Mutation):
    """Create Referee Graphql"""
    referee = Field(lambda: RefereeNode,
                    description="Referee created by this mutation.")

    class Arguments:
        """Create Referee Arguments"""
        referee_data = CreateRefereeInput(required=True)

    def mutate(self, info, referee_data=None):
        """Create Referee Graphql"""
        data = input_to_dictionary(referee_data)

        referee = RefereeModel(**data)
        referee_db = DB.session.query(RefereeModel).filter_by(
            description=data['description']).first()
        if referee_db:
            print('need to update')
            referee_db = referee
        else:
            DB.session.add(referee)
        DB.session.commit()

        return CreateReferee(referee=referee)


class UpdateRefereeInput(InputObjectType, RefereeAttribute):
    """Update Referee Input fields derived from RefereeAttribute"""
    id = ID(required=True, description="Global Id of the Referee.")


class UpdateReferee(Mutation):
    """Update Referee Graphql"""
    referee = Field(lambda: RefereeNode,
                    description="Referee updated by this mutation.")

    class Arguments:
        """Arguments for Update Referee"""
        referee_data = UpdateRefereeInput(required=True)

    def mutate(self, info, referee_data):
        """Update Referee Graphql"""
        data = input_to_dictionary(referee_data)

        referee = DB.session.query(RefereeModel).filter_by(id=data['id']).first()
        referee.update(data)
        DB.session.commit()
        referee = DB.session.query(RefereeModel).filter_by(id=data['id']).first()

        return UpdateReferee(referee=referee)
