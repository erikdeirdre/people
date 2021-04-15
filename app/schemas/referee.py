""" Graphql Referee Schema Module """
from graphene import (String, Boolean, ID, InputObjectType, Field,
                      Mutation, Connection, Node, List, InputField)
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.filters import FilterConnectionField

from helpers.utils import (input_to_dictionary)
from app import (DB)
from app.database import (Referee as RefereeModel, Sport, RefereeSport,
                          Level)
from .helpers import (TotalCount, Sports, CreateSportsInput)

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
            level = None
            level_date = None
            level_years = 0
            description = None
            active = False
            if row.RefereeSport.level:
                level = row.RefereeSport.level.description
                level_date = row.RefereeSport.level_date
                level_years = row.RefereeSport.years_level
                description = row.Sport.description
                active = row.RefereeSport.active

            sports.append({'id': row.Sport.id,
                           'description': description,
                           'active': active,
                           'level': level,
                           'level_date': level_date,
                           'level_years': level_years})
        return sports


class RefereeConnection(Connection):
    """ Referee Connection """
    class Meta:
        """ Referee Connection """
        node = RefereeNode
        interfaces = (TotalCount,)


class CreateRefereeInput(InputObjectType, RefereeAttribute):
    """Create Referee Input fields derived from RefereeAttribute"""
    sport = InputField(CreateSportsInput)
    print('wait')


class CreateReferee(Mutation):
    """Create Referee Graphql"""
    referee = Field(lambda: RefereeNode,
                    description="Referee created by this mutation.")
    ok = Boolean()

    class Arguments:
        """Create Referee Arguments"""
        referee_data = CreateRefereeInput(required=True)
        sport_data = CreateSportsInput()

    def mutate(self, info, referee_data=None, sport_data=None):
        """Create Referee Graphql"""
        ref_data = input_to_dictionary(referee_data)
        referee = RefereeModel(**ref_data)
        referee_db = DB.session.query(RefereeModel).filter_by(
            email=ref_data['email']).first()
        if referee_db:
            print('need to update')
            referee_db = referee
        else:
            DB.session.add(referee)

        data = input_to_dictionary(sport_data)
        # Description isn't part of RefereeSport Model, so pull out the field
        description = data.pop('description')
        # Level returns as string, need to get Level Object
        level = DB.session.query(Level).filter_by(description=data['level']).first()
        if level:
            data['level'] = level
        else:
            print('need no level logic')
        sport = RefereeSport(**data)
        sport_db = DB.session.query(Sport, RefereeSport).join(Sport).filter(
            Sport.description == description).first()
        if sport_db:
            print('need to update')
        else:
            DB.session.add(sport)
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
