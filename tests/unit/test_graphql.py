""" Unit Test Module for Graphql """
import sys
from os.path import (join, abspath, dirname)
from glob import glob
from json import (loads, dumps)
import unittest
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
import pytest
from graphene.test import Client
from testclass.testclass import TestClass
from app import DB
from app.schema import schema


@pytest.fixture(scope='class')
def init_database():
    """Initializes the database """
    DB.drop_all()
    DB.create_all()

    base_dir = join(abspath(dirname(__file__)),  '..', '..')
    print("base dir: {}".format(base_dir))

    for fixture_file in glob(join(base_dir, 'fixtures', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)

    for fixture_file in glob(join(base_dir, 'fixtures', 'demo', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)

    yield DB
    DB.drop_all()


@pytest.mark.usefixtures("init_database")
class TestSchema(unittest.TestCase):
    """Test Suite for testing Schema"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(schema)

    def test_sport_list(self):
        """Execute sport listing test"""
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)

        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        print(dumps(executed['data']))

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

    def test_referee_query(self):
        """Execute referee query test"""
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

    def test_coach_query(self):
        """Execute coach query test"""
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])
"""
    def test_referee_attribute_query(self):
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

    def test_coach_query(self):
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])
"""

if __name__ == '__main__':
    unittest.main()
