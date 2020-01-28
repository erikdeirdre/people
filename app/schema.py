import graphene
from graphene import relay
from graphene_sqlalchemy import (SQLAlchemyObjectType,
                                 SQLAlchemyConnectionField)

from helpers.utils import (input_to_dictionary)
from app import db
from .database import (Person as PersonModel, Sport as SportModel,
                       Referee as RefereeModel, Coach as CoachModel)

__all__ = ['CreatePerson', 'UpdatePerson', 'CreateSport']


class CoachAttribute:
    sport = graphene.String()
    grade = graphene.String()
    active = graphene.Boolean()


class Coach(SQLAlchemyObjectType):
    class Meta:
        model = CoachModel
        interfaces = (relay.Node,)


class CreateCoachInput(graphene.InputObjectType, CoachAttribute):
    pass


class RefereeAttribute:
    sport = graphene.String()
    grade = graphene.String()
    active = graphene.Boolean()


class Referee(SQLAlchemyObjectType):
    class Meta:
        model = RefereeModel
        interfaces = (relay.Node,)


class CreateRefereeInput(graphene.InputObjectType, RefereeAttribute):
    pass


class CreateReferee(graphene.Mutation):
    person = graphene.Field(lambda: Referee,
                             description="Referee created by this mutation.")

    class Arguments:
        referee_data = CreateRefereeInput(required=True)

    @staticmethod
    def mutate(self, info, sport_data=None):
        data = input_to_dictionary(referee_data)

        referee = RefereeModel(**data)
        referee_db = SportModel.query.filter_by(description=data['email']).first()
        if referee_db:
            print('need to update')
            referee_db = referee
        else:
            db.session.add(referee)
        db.session.commit()

        return CreateReferee(referee=referee)


class SportAttribute:
    description = graphene.String()
    active = graphene.Boolean()


class Sport(SQLAlchemyObjectType, SportAttribute):
    class Meta:
        model = SportModel
        interfaces = (relay.Node,)


class CreateSportInput(graphene.InputObjectType, SportAttribute):
    pass


class CreateSport(graphene.Mutation):
    person = graphene.Field(lambda: Sport,
                             description="Person created by this mutation.")

    class Arguments:
        sport_data = CreateSportInput(required=True)

    @staticmethod
    def mutate(self, info, sport_data=None):
        data = input_to_dictionary(sport_data)

        sport = SportModel(**data)
        sport_db = SportModel.query.filter_by(description=data['description']).first()
        if sport_db:
            print('need to update')
            sport_db = sport
        else:
            db.session.add(sport)
        db.session.commit()

        return CreateSport(sport=sport)


class UpdateSportInput(graphene.InputObjectType, SportAttribute):
    id = graphene.ID(required=True, description="Global Id of the Sport.")


class UpdateSport(graphene.Mutation):
    sport = graphene.Field(lambda: Sport, description="Sport updated by this mutation.")

    class Arguments:
        sport_data = UpdateSportInput(required=True)

    @staticmethod
    def mutate(self, info, sport_data):
        data = input_to_dictionary(sport_data)

        sport = db.session.query(PersonModel).filter_by(id=data['id'])
        sport.update(data)
        db.session.commit()
        sport = db.session.query(PersonModel).filter_by(id=data['id']).first()

        return UpdateSport(sport=sport)


class PersonAttribute:
    first_name = graphene.String()
    last_name = graphene.String()
    address1 = graphene.String()
    address2 = graphene.String()
    city = graphene.String()
    state = graphene.String()
    zip_code = graphene.String()
    telephone = graphene.String()
    email = graphene.String(required=True)
    gender = graphene.String()
    birth_date = graphene.String()
    age = graphene.Int()


class Person(SQLAlchemyObjectType, PersonAttribute):
    class Meta:
        model = PersonModel
        interfaces = (relay.Node,)


class CreatePersonInput(graphene.InputObjectType, PersonAttribute):
    pass


class CreatePerson(graphene.Mutation):
    person = graphene.Field(lambda: Person,
                             description="Person created by this mutation.")

    class Arguments:
        person_data = CreatePersonInput(required=True)

    @staticmethod
    def mutate(self, info, person_data=None):
        data = input_to_dictionary(person_data)

        person = PersonModel(**data)
        person_db = PersonModel.query.filter_by(email=data['email']).first()
        if person_db:
            print('need to update')
            person_db = person
        else:
            db.session.add(person)
        db.session.commit()

        return CreatePerson(person=person)


class UpdatePersonInput(graphene.InputObjectType, PersonAttribute):
    id = graphene.ID(required=True, description="Global Id of the Person.")


class UpdatePerson(graphene.Mutation):
    person = graphene.Field(lambda: Person, description="Person updated by this mutation.")

    class Arguments:
        person_data = UpdatePersonInput(required=True)

    @staticmethod
    def mutate(self, info, person_data):
        data = input_to_dictionary(person_data)

        person = db.session.query(PersonModel).filter_by(id=data['id'])
        person.update(data)
        db.session.commit()
        person = db.session.query(PersonModel).filter_by(id=data['id']).first()

        return UpdatePerson(person=person)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    personList = SQLAlchemyConnectionField(Person)
    sportList = SQLAlchemyConnectionField(Sport)
    refereeList = SQLAlchemyConnectionField(Referee)
    coachList = SQLAlchemyConnectionField(Coach)


class Mutation(graphene.ObjectType):
    createPerson = CreatePerson.Field()
    createReferee = CreateReferee.Field()
    updatePerson = UpdatePerson.Field()
    createSport = CreateSport.Field()
    updateSport = UpdateSport.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
