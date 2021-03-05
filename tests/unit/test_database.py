from datetime import date
import unittest
import pytest
from os.path import (abspath, dirname, join)
from glob import glob
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
from app import db
from app.database import (Team, Sport, Person, Referee, Coach)


@pytest.fixture(scope='class')
def init_database():
    """Initializes the database """
   DB.drop_all()
   DB.create_all()

    base_dir = join(abspath(dirname(__file__)),  '..', '..')
    print("base dir: {}".format(base_dir))

    for fixture_file in glob(join(base_dir, 'fixtures', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(db, fixtures)

    for fixture_file in glob(join(base_dir, 'fixtures', 'demo', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(db, fixtures)

    yield db
   DB.drop_all()


@pytest.mark.usefixtures("init_database")
class TestSportTable(unittest.TestCase):
    def test_sport_all(self):
    """Test Query gets correct number of rows"""
        result = db.session.query(Sport).all()
        self.assertEqual(len(result), 3, "Not equal to three sports rows")

    def test_sport_active_true(self):
    """Test to check active, true"""
        result = db.session.query(Sport).filter_by(description="Soccer").first()
        self.assertEqual(result.active, True)

    def test_sport_active_false(self):
    """Test to check active, false"""
        result = db.session.query(Sport).filter_by(description="Baseball").first()
        self.assertEqual(result.active, False)


@pytest.mark.usefixtures("init_database")
class TestPersonTable(unittest.TestCase):
    def test_person_all(self):
    """Test Query gets correct number of rows"""
        result = db.session.query(Person).all()
        self.assertEqual(len(result), 3, "Not equal to three person rows")

    def test_person(self):
    """Test to confirm columns return correctly"""
        dt = date(1950, 1, 1)
        result = db.session.query(Person).filter_by(last_name="Mouse").first()
        self.assertEqual(result.address1, "1 Disney Lane")
        self.assertEqual(result.address2, "2 Disney Lane")
        self.assertEqual(result.first_name, "Mickey")
        self.assertEqual(result.last_name, "Mouse")
        self.assertEqual(result.city, "Orlando")
        self.assertEqual(result.state, "FL")
        self.assertEqual(result.zip_code, "12345")
        self.assertEqual(result.telephone, "1234567890")
        self.assertEqual(result.email, "mickey@sample.com")
        self.assertEqual(result.gender, "Male")
        self.assertEqual(result.birth_date, dt)

@pytest.mark.usefixtures("init_database")
class TestRefereeTable(unittest.TestCase):
    def test_referee_all(self):
        """Test Query gets correct number of rows"""
        result = db.session.query(Referee).all()
        self.assertEqual(len(result), 3, "Not equal to three person rows")

    def test_referee(self):
        """Test to confirm columns return correctly"""
        result = db.session.query(Referee).get(1)
        self.assertEqual(result.active, True)
#        self.assertEqual(result.city, 'Orlando')
#        self.assertEqual(result.grade, 'junior')
#        self.assertEqual(result.sportId, 1)
#        result = db.session.query(Referee).get(2)
#        self.assertEqual(result.active, False)
#        self.assertEqual(result.city, 'Springfield')
#        self.assertEqual(result.grade, 'junior')
#        self.assertEqual(result.sportId, 1)
#
@pytest.mark.usefixtures("init_database")
class TestCoachTable(unittest.TestCase):
    def test_referee_all(self):
        """Test Query gets correct number of rows"""
        result = db.session.query(Referee).all()
        self.assertEqual(len(result), 3, "Not equal to three person rows")
    def test_coach(self):
        """Test to confirm columns return correctly"""
        result = db.session.query(Coach).get(1)
        self.assertEqual(result.active, True)
#        self.assertEqual(result.city, 'Orlando')
#        self.assertEqual(result.grade, 'junior')
#        self.assertEqual(result.sportId, 1)
#        result = db.session.query(Coach).get(2)
#        self.assertEqual(result.active, False)
#        self.assertEqual(result.city, 'Springfield')
#        self.assertEqual(result.grade, 'junior')
#        self.assertEqual(result.sportId, 1)
#
if __name__ == '__main__':
    unittest.main()
