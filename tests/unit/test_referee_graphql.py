""" Unit Test Module for Graphql """
import sys
from os.path import (join, abspath, dirname)
from glob import glob
from json import (loads, dumps)
import unittest
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
from graphene.test import Client
from testclass.testclass import TestClass
from app import DB
from app.schema import SCHEMA


def init_database():
    """Initializes the database """
    DB.drop_all()
    DB.create_all()

    base_dir = join(abspath(dirname(__file__)), '..', '..')

    for fixture_file in glob(join(base_dir, 'seed', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)

    for fixture_file in glob(join(base_dir, 'seed', 'demo', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)


class TestRefereeGraphGL(unittest.TestCase):
    """Test Suite for testing Referee GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)

    def setUp(self):
        """Initialize the database"""
        init_database()

    def test_referee_list(self):
        """Execute referee query test"""
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        print(dumps(executed['data']))
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

#    def test_referee_attribute_query(self):
#        test_data = TestClass(self.dir_name,
#                              sys._getframe(  ).f_code.co_name)
#        test_data.load_files()

#        executed = self.client.execute(test_data.get_send_request())
#        self.assertEqual(loads(dumps(executed['data'])),
#                         test_data.get_expected_result()['data'])


if __name__ == '__main__':
    unittest.main()
