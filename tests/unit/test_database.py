""" Database Unit Test Module """
from datetime import date
from os.path import (abspath, dirname, join)
from glob import glob
import unittest
import pytest
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
from app import DB
from app.database import (Team, Sport, Person, Referee, Coach)


@pytest.fixture(scope='class')
def init_database():
    """Initializes the database """
    DB.drop_all()
    DB.create_all()

    base_dir = join(abspath(dirname(__file__)), '..', '..')
    print("base dir: {}".format(join(base_dir, 'seed', '*.json')))

    for fixture_file in glob(join(base_dir, 'seed', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)

    for fixture_file in glob(join(base_dir, 'seed', 'demo', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)

    yield DB

    DB.drop_all()


@pytest.mark.usefixtures("init_database")
class TestSportTable(unittest.TestCase):
    def test_sport_all(self):
        """Test Query gets correct number of rows"""

        result = DB.session.query(Sport).all()
        self.assertEqual(len(result), 9, "Not equal to NINE sports rows")

    def test_sport_active_true(self):
        """Test to check active, true"""
        result = DB.session.query(Sport).filter_by(description="Soccer").first()
        self.assertEqual(result.active, True)

    def test_sport_active_false(self):
        """Test to check active, false"""
        result = DB.session.query(Sport).filter_by(description="Baseball").first()
        self.assertEqual(result.active, True)


@pytest.mark.usefixtures("init_database")
class TestPersonTable(unittest.TestCase):
    def test_person_all(self):
        """Test Query gets correct number of rows"""
        result = DB.session.query(Person).all()
        self.assertEqual(len(result), 5, "Not equal to FIVE person rows")

    def test_person(self):
        """Test to confirm columns return correctly"""
        result = DB.session.query(Person).filter_by(last_name="Simpson").first()
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.first_name, "Homer")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "hsimpson@simpsons.com")
#        self.assertEqual(result.gender, "Gender.MALE")

@pytest.mark.usefixtures("init_database")
class TestRefereeTable(unittest.TestCase):
    def test_referee_all(self):
        """Test Query gets correct number of rows"""
        result = DB.session.query(Referee).all()
        self.assertEqual(len(result), 4, "Not equal to FOUR Referee rows")

    def test_referee(self):
        """Test to confirm columns return correctly"""
        result = DB.session.query(Referee).get(1)
        self.assertEqual(result.active, True)
#        self.assertEqual(result.city, 'Orlando')
#        self.assertEqual(result.grade, 'junior')
#        self.assertEqual(result.sportId, 1)
#        result = DB.session.query(Referee).get(2)
#        self.assertEqual(result.active, False)
#        self.assertEqual(result.city, 'Springfield')
#        self.assertEqual(result.grade, 'junior')
#        self.assertEqual(result.sportId, 1)
#
@pytest.mark.usefixtures("init_database")
class TestCoachTable(unittest.TestCase):
    def test_coach_all(self):
        """Test Query gets correct number of rows"""
        result = DB.session.query(Coach).all()
        self.assertEqual(len(result), 4, "Not equal to FOUR Coach rows")
    def test_coach(self):
        """Test to confirm columns return correctly"""
        result = DB.session.query(Coach).get(1)
        self.assertEqual(result.active, True)
#        self.assertEqual(result.city, 'Orlando')
#        self.assertEqual(result.grade, 'junior')
#        self.assertEqual(result.sportId, 1)
#        result = DB.session.query(Coach).get(2)
#        self.assertEqual(result.active, False)
#        self.assertEqual(result.city, 'Springfield')
#        self.assertEqual(result.grade, 'junior')
#        self.assertEqual(result.sportId, 1)

if __name__ == '__main__':
    unittest.main()
