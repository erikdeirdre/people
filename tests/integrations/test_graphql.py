import sys
from os.path import (join, abspath, dirname)
from json import (loads, dumps)
import unittest
import pytest
from graphene.test import Client
from testclass.testclass import TestClass
from app import db
from app.schema import schema


@pytest.fixture(scope='class')
def init_database():
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
class TestSchema(unittest.TestCase):
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(schema)

    def test_food_query(self):
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

    def test_food_attribute_query(self):
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

    def test_food_category_query(self):
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

    def test_branded_food_query(self):
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])


if __name__ == '__main__':
    unittest.main()
