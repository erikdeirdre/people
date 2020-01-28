from datetime import date
import unittest
import pytest
from app import db
from app.database import (Sport, Person, Referee, Coach)


@pytest.fixture(scope='class')
def init_database():
    from os.path import (abspath, dirname, join)
    from glob import glob
    from flask_fixtures.loaders import JSONLoader
    from flask_fixtures import load_fixtures

    db.drop_all()
    db.create_all()

    base_dir = abspath(dirname(__file__))

    for fixture_file in glob(join(base_dir, 'fixtures', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(db, fixtures)

    yield db
    db.drop_all()


@pytest.mark.usefixtures("init_database")
class TestSportTable(unittest.TestCase):
    def test_sport_all(self):
        result = db.session.query(Sport).all()
        self.assertEqual(len(result), 3, "Not equal to three sports rows")

    def test_sport_active_true(self):
        result = db.session.query(Sport).filter_by(description="Soccer").one()
        self.assertEqual(result.active, True)

    def test_sport_active_false(self):
        result = db.session.query(Sport).filter_by(description="Baseball").one()
        self.assertEqual(result.active, False)

    def test_sport_active_not_set(self):
        result = db.session.query(Sport).filter_by(description="Football").one()
        self.assertEqual(result.active, None)


@pytest.mark.usefixtures("init_database")
class TestPersonTable(unittest.TestCase):
    def test_person_all(self):
        result = db.session.query(Person).all()
        self.assertEqual(len(result), 3, "Not equal to three person rows")

    def test_person(self):
        dt = date(1950, 1, 1)
        result = db.session.query(Person).filter_by(last_name="Mouse").one()
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

    def test_referee(self):
        result = db.session.query(Referee).get(1)
        self.assertEqual(result.active, True)
        self.assertEqual(result.city, 'Orlando')
        self.assertEqual(result.grade, 'junior')
        self.assertEqual(result.sportId, 1)
        result = db.session.query(Referee).get(2)
        self.assertEqual(result.active, False)
        self.assertEqual(result.city, 'Springfield')
        self.assertEqual(result.grade, 'junior')
        self.assertEqual(result.sportId, 1)

    def test_coach(self):
        result = db.session.query(Coach).get(1)
        self.assertEqual(result.active, True)
        self.assertEqual(result.city, 'Orlando')
        self.assertEqual(result.grade, 'junior')
        self.assertEqual(result.sportId, 1)
        result = db.session.query(Coach).get(2)
        self.assertEqual(result.active, False)
        self.assertEqual(result.city, 'Springfield')
        self.assertEqual(result.grade, 'junior')
        self.assertEqual(result.sportId, 1)

if __name__ == '__main__':
    unittest.main()
