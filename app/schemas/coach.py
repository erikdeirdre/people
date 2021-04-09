""" Graphql Coach Schema Module """
from graphene import (String, Boolean, ID, InputObjectType, Node,
                      Field, Mutation, Connection, List)
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.filters import FilterConnectionField

from helpers.utils import (input_to_dictionary)
from app import (DB)
from app.database import (Coach as CoachModel, Sport, CoachSport,
                          CoachTeam, Team)
from .helpers import (TotalCount, Sports, Teams)


class CoachNode(SQLAlchemyObjectType):
    """ Coach Node """
    class Meta:
        """ Coach Node """
        model = CoachModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory

    sport = List(Sports)
    team = List(Teams)

    def resolve_sport(self, info):
        ''' sport resolver '''
        sports = []
        results = DB.session.query(CoachSport, Sport).join(Sport).filter(
            CoachSport.coach_id == self.id)
        for row in results:
            achieve = None
            achieve_date = None
            achieve_years = 0
            description = None
            active = False
            if row.CoachSport.level:
                achieve = row.CoachSport.level.description
                achieve_date = row.CoachSport.level_date
                achieve_years = row.CoachSport.years_level
                description = row.Sport.description
                active = row.CoachSport.active

            sports.append({'id': row.Sport.id,
                           'description': description,
                           'active': active,
                           'achieve': achieve,
                           'achieve_date': achieve_date,
                           'achieve_years': achieve_years})
        return sports

    def resolve_team(self, info):
        ''' team resolver '''
        teams = []
        results = DB.session.query(CoachTeam, Team).join(Team).filter(
            CoachTeam.coach_id == self.id)
        for row in results:
            join_date = None
            join_years = 0
            active = False
            description = None

            if row.CoachTeam.active:
                join_date = row.CoachTeam.join_date
                join_years = row.CoachTeam.years_active
                active = row.CoachTeam.active
                description = row.Team.description
            teams.append({'id': row.Team.id,
                           'description': description,
                           'active': active,
                           'join_date': join_date,
                           'join_years': join_years})
        return teams

class CoachConnection(Connection):
    """Coach Graphql Query output"""
    class Meta:
        """Coach Graphql Query output"""
        node = CoachNode
        interfaces = (TotalCount,)


class CoachAttribute:
    """Coach Input Template """
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
    team = String()


class CreateCoachInput(InputObjectType, CoachAttribute):
    """Create Coach Input fields derived from CoachAttribute"""


class CreateCoach(Mutation):
    """Create Coach Graphql"""
    coach = Field(lambda: CoachNode,
                  description="Coach created by this mutation.")

    class Arguments:
        """Arguments for Create Coach"""
        coach_data = CreateCoachInput(required=True)

    def mutate(self, info, coach_data=None):
        """Create Coach Graphql"""
        data = input_to_dictionary(coach_data)

        coach = CoachModel(**data)
        coach_db = DB.session.query(CoachModel).filter_by(
            description=data['description']).first()
        if coach_db:
            print('need to update')
            coach_db = coach
        else:
            DB.session.add(coach)
        DB.session.commit()

        return CreateCoach(coach=coach)


class UpdateCoachInput(InputObjectType, CoachAttribute):
    """Update Coach Input fields derived from CoachAttribute"""
    id = ID(required=True, description="Global Id of the Coach.")


class UpdateCoach(Mutation):
    """Update Coach Graphql"""
    coach = Field(lambda: CoachNode,
                  description="Coach updated by this mutation.")

    class Arguments:
        """Arguments for Update Coach"""
        coach_data = UpdateCoachInput(required=True)

    def mutate(self, info, coach_data):
        """Update Coach Graphql"""
        data = input_to_dictionary(coach_data)

        coach = DB.session.query(CoachModel).filter_by(id=data['id']).first()
        coach.update(data)
        DB.session.commit()
        coach = DB.session.query(CoachModel).filter_by(id=data['id']).first()

        return UpdateCoach(coach=coach)
