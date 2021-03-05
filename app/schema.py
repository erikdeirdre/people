""" Graphql Schema Module """
import requests
import xmltodict

from graphene import (ObjectType, String, Boolean, ID, InputObjectType,
                      Field, relay, Schema, Argument, Mutation, Interface)
from graphene_sqlalchemy import (SQLAlchemyObjectType,
                                 SQLAlchemyConnectionField)

from helpers.utils import (input_to_dictionary)
from app import (DB, PO_URL, PO_USERID)
from .database import (Sport as SportModel, Team as TeamModel,
                       Person as PersonModel, Coach as CoachModel,
                       Referee as RefereeModel)

#__all__ = ['CreatePerson', 'UpdatePerson']


def postal_code_request(postal_code):
    """API call to USPS system to retrieve city state based on zip code."""
    url = '{}?API=CityStateLookup&XML=<CityStateLookupRequest USERID="{}">' \
          '<ZipCode ID=\'0\'><Zip5>{}</Zip5></ZipCode>'  \
          '</CityStateLookupRequest>'.format(PO_URL, PO_USERID,
                                             postal_code)

    results = requests.get(url)
    if results.status_code == 200:
        response = xmltodict.parse(results.text)["CityStateLookupResponse"]["ZipCode"]
        if 'Error' in response:
            return {'error': response['Error']['Description']}
        return {'postalcode': postal_code, 'city': response["City"],
                'state': response["State"]}

    return None

def verify_address_request(postal_code, address1, address2, city, state):
    """API call to USPS system to verify address against zip code."""
    url = '{}?API=Verify&XML=<AddressValidateRequest USERID="{}">' \
        '<Address><Address1>{}</Address1><Address2>{}</Address2>' \
        '<City>{}</City><State>{}</State><Zip5>{}</Zip5><Zip4></Zip4>' \
        '</Address></AddressValidateRequest>'.format(PO_URL, PO_USERID,
                                                     address2, address1,
                                                     city, state,
                                                     postal_code)

    results = requests.get(url)
    if results.status_code == 200:
        response = xmltodict.parse(results.text)["AddressValidateResponse"] \
                                                ["Address"]
        if 'Error' in response:
            return {'error': response['Error']['Description']}

        if 'Zip4' in response:
            postal_code = '{}-{}'.format(response['Zip5'], response['Zip4'])
        else:
            postal_code = response['Zip5']
# API uses Address2 as the primary address field
        if 'Address1'in response:
            address1 = response['Address1']
            address2 = response['Address2']
        else:
            address1 = response['Address2']
            address2 = None

        return {'postalcode': postal_code, 'city': response["City"],
                'state': response["State"], 'address1': address1,
                'address2': address2}

    return {'postalcode': None, 'city': None, 'state': None,
            'address1': None, 'address2': None}

def resolve_address(postalcode, address1, address2='', city='', state=''):
    """Verify / cleanup address based on USPS information. """
    address = verify_address_request(postalcode, address1, address2, city,
                                     state)
    return Address(
        postalcode=postalcode,
        city=address['city'],
        state=address['state'],
        address1=address['address1'],
        address2=address['address2']
    )


def resolve_city_states(postalcode):
    """Get city / state from USPS based on zip code. """
    city_state = postal_code_request(postalcode)
    return CityState(
        postalcode=postalcode,
        city=city_state['city'],
        state=city_state['state']
    )


class Address(ObjectType):
    postalcode = String()
    city = String()
    state = String()
    address1 = String()
    address2 = String()


class CityState(ObjectType):
    postalcode = String() 
    city = String()
    state = String()


class TeamAttribute(Interface):
    description = String()
    active = Boolean()


class Team(SQLAlchemyObjectType):
    class Meta:
        model = TeamModel
        interfaces = (relay.Node, TeamAttribute,)


class CreateTeamInput(InputObjectType, TeamAttribute):
    pass


class CreateTeam(Mutation):
    team = Field(lambda: Team,
                 description="Team created by this mutation.")

    class Arguments:
        team_data = CreateTeamInput(required=True)

    @staticmethod
    def mutate(team_data=None):
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
    id = ID(required=True, description="Global Id of the Team.")


class UpdateTeam(Mutation):
    team = Field(lambda: Team, description="Team updated by this mutation.")

    class Arguments:
        team_data = UpdateTeamInput(required=True)

    @staticmethod
    def mutate(team_data):
        data = input_to_dictionary(team_data)

        team = DB.session.query(TeamModel).filter_by(id=data['id'])
        team.update(data)
        DB.session.commit()
        team = DB.session.query(TeamModel).filter_by(id=data['id']).first()

        return UpdateTeam(team=team)


class CoachAttribute:
    sport = String()
    grade = String()
    active = Boolean()
    team = String()


class Coach(SQLAlchemyObjectType):
    class Meta:
        model = CoachModel
        interfaces = (relay.Node,)


class CreateCoachInput(InputObjectType, CoachAttribute):
    pass


class CreateCoach(Mutation):
    coach = Field(lambda: Coach,
                  description="Coach created by this mutation.")

    class Arguments:
        coach_data = CreateCoachInput(required=True)

    @staticmethod
    def mutate(coach_data=None):
        data = input_to_dictionary(coach_data)

        coach = CoachModel(**data)
        coach_db = DB.session.query(CoachModel).filter_by(
            description=data['description']).first()
        if coach_db:
            print('need to update')
            referee_db = coach
        else:
            DB.session.add(coach)
        DB.session.commit()

        return CreateCoach(coach=coach)


class UpdateCoachInput(InputObjectType, CoachAttribute):
    id = ID(required=True, description="Global Id of the Coach.")


class UpdateCoach(Mutation):
    coach = Field(lambda: Coach, 
                  description="Coach updated by this mutation.")

    class Arguments:
        coach_data = UpdateCoachInput(required=True)

    @staticmethod
    def mutate(coach_data):
        data = input_to_dictionary(coach_data)

        coach = DB.session.query(CoachModel).filter_by(id=data['id']).first()
        coach.update(data)
        DB.session.commit()
        coach = DB.session.query(CoachModel).filter_by(id=data['id']).first()

        return UpdateCoach(coach=coach)


#class RefereeAttribute:
#    sport = String()
#    grade = String()
#    active = Boolean()
#
#
class Referee(SQLAlchemyObjectType):
    class Meta:
        model = RefereeModel
        interfaces = (relay.Node,)


#class CreateRefereeInput(graphene.InputObjectType, RefereeAttribute):
#    pass
#
#
#class CreateReferee(graphene.Mutation):
#    person = Field(lambda: Referee,
#                             description="Referee created by this mutation.")
#
#    class Arguments:
#        referee_data = CreateRefereeInput(required=True)
#
#    @staticmethod
#    def mutate(self, info, referee_data=None):
#        data = input_to_dictionary(referee_data)
#
#        referee = RefereeModel(**data)
#        referee_db = DB.session.query(SportModel).filter_by(description=data['description']).first()
#        if referee_db:
#            print('need to update')
#            referee_db = referee
#        else:
#            DB.session.add(referee)
#        DB.session.commit()
#
#        return CreateReferee(referee=referee)
#

class SportAttribute:
    description = String()
    active = Boolean()


class Sport(SQLAlchemyObjectType, SportAttribute):
    class Meta:
        model = SportModel
        interfaces = (relay.Node,)


class CreateSportInput(InputObjectType, SportAttribute):
    pass

'''
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
'''
class CreateSport(Mutation):
    sport = Field(lambda: Sport,
                  description="Sport created by this mutation.")

    class Arguments:
        sport_data = CreateSportInput(required=True)

    @staticmethod
    def mutate(sport_data=None):
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
    sport = Field(lambda: Sport,
                  description="Sport updated by this mutation.")

    class Arguments:
        sport_data = UpdateSportInput(required=True)

    @staticmethod
    def mutate(self, info, sport_data):
        data = input_to_dictionary(sport_data)

        sport = DB.session.query(SportModel).filter_by(id=data['id'])
        sport.update(data)
        DB.session.commit()
        sport = DB.session.query(SportModel).filter_by(id=data['id']).first()

        return UpdateSport(sport=sport)


class PersonAttribute:
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


class Person(SQLAlchemyObjectType):
    class Meta:
        model = PersonModel
        interfaces = (relay.Node,)


class CreatePersonInput(InputObjectType, PersonAttribute):
    pass


#class CreatePerson(graphene.Mutation):
#    person = Field(lambda: Person,
#                             description="Person created by this mutation.")
#
#    class Arguments:
#        person_data = CreatePersonInput(required=True)
#
#    @staticmethod
#    def mutate(self, info, person_data=None):
#        data = input_to_dictionary(person_data)
#
#        person = PersonModel(**data)
#        person_db = PersonModel.query.filter_by(email=data['email']).first()
#        if person_db:
#            print('need to update')
#            person_db = person
#        else:
#            DB.session.add(person)
#        DB.session.commit()
#
#        return CreatePerson(person=person)
#
#
#class UpdatePersonInput(graphene.InputObjectType, PersonAttribute):
#    id = ID(required=True, description="Global Id of the Person.")
#
#
#class UpdatePerson(graphene.Mutation):
#    person = Field(lambda: Person, description="Person updated by this mutation.")
#
#    class Arguments:
#        person_data = UpdatePersonInput(required=True)
#
#    @staticmethod
#    def mutate(self, info, person_data):
#        data = input_to_dictionary(person_data)
#
#        person = DB.session.query(PersonModel).filter_by(id=data['id'])
#        person.update(data)
#        DB.session.commit()
#        person = DB.session.query(PersonModel).filter_by(id=data['id']).first()
#
#        return UpdatePerson(person=person)
#

#class Player(ObjectType):
#    birth_date = String()
#    age = Int()
#    sport = String()
#

class Query(ObjectType):
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

    coachList = SQLAlchemyConnectionField(Coach)
    personList = SQLAlchemyConnectionField(Person)
    sportList = SQLAlchemyConnectionField(Sport)
    teamList = SQLAlchemyConnectionField(Team)
    refereeList = SQLAlchemyConnectionField(Referee)


class Mutation(ObjectType):
#    createPerson = CreatePerson.Field()
#    updatePerson = UpdatePerson.Field()
 #   createReferee = CreateReferee.Field()
    createCoach = CreateCoach.Field()
    updateCoach = UpdateCoach.Field()
    createSport = CreateSport.Field()
    updateSport = UpdateSport.Field()
    createTeam = CreateTeam.Field()
    updateTeam = UpdateTeam.Field()

schema = Schema(query=Query, mutation=Mutation)
