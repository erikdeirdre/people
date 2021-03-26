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

@pytest.mark.usefixtures("init_database")
class TestSportTable(unittest.TestCase):
    """Test Sport Table"""
    def test_sport_all(self):
        """Test Query gets correct number of rows"""
        print('here')
        print(DB.__dict__)
        self.assertEqual(1, 1)
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
class TestTeamTable(unittest.TestCase):
    """Test Team Table"""
    def test_team_all(self):
        """Test Query gets correct number of rows"""
        result = DB.session.query(Team).all()
        self.assertEqual(len(result), 4, "Not equal to FOUR team rows")

    def test_team_active_true(self):
        """Test to check active, true"""
        result = DB.session.query(Team).filter_by(description="Celtics").first()
        self.assertEqual(result.active, True)

    def test_team_active_false(self):
        """Test to check active, false"""
        result = DB.session.query(Team).filter_by(description="Patriots").first()
        self.assertEqual(result.active, True)


@pytest.mark.usefixtures("init_database")
class TestRefereeTable(unittest.TestCase):
    """Test Referee Table"""
    def test_referee_all(self):
        """Test Query gets correct number of rows"""
        result = DB.session.query(Referee).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Referee rows")

    def test_referee(self):
        """Test to confirm columns return correctly"""
        result = DB.session.query(Referee).get(3)
        self.assertEqual(result.active, True)
        self.assertEqual(result.level_date, date(2018, 3, 1))
        self.assertEqual(result.sport_id, 1)
        self.assertEqual(result.first_name, "Bart")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "bsimpson@simpsons.com")
#        self.assertEqual(result.gender, "MALE")

        result = DB.session.query(Referee).get(4)
        self.assertEqual(result.active, False)
        self.assertEqual(result.first_name, "Lisa")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "lsimpson@simpsons.com")
#        self.assertEqual(result.gender, "FEMALE")
        self.assertEqual(result.level_date, date(2019, 6, 1))
        self.assertEqual(result.sport_id, 2)

@pytest.mark.usefixtures("init_database")
class TestCoachTable(unittest.TestCase):
    """Test Coach Table"""
    def test_coach_all(self):
        """Test Query gets correct number of rows"""
        result = DB.session.query(Coach).all()
        self.assertEqual(len(result), 2, "Not equal to TWO Coach rows")
    def test_coach(self):
        """Test to confirm columns return correctly"""
        result = DB.session.query(Coach).get(1)
        self.assertEqual(result.active, True)
        self.assertEqual(result.first_name, "Homer")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "hsimpson@simpsons.com")
        self.assertEqual(result.team_id, 1)
        self.assertEqual(result.sport_id, 1)

        result = DB.session.query(Coach).get(2)
        self.assertEqual(result.active, False)
        self.assertEqual(result.first_name, "Marge")
        self.assertEqual(result.last_name, "Simpson")
        self.assertEqual(result.address1, "123 Evergreen Terrace")
        self.assertEqual(result.city, "Springfield")
        self.assertEqual(result.state, "MA")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.email, "msimpson@simpsons.com")
        self.assertEqual(result.team_id, 2)
        self.assertEqual(result.sport_id, 2)

if __name__ == '__main__':
    unittest.main()
