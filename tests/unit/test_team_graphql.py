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


class TestTeamGraphGL(unittest.TestCase):
    """Test Suite for testing Sport GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)

    def setUp(self):
        """Initialize the database"""
        init_database()

    def test_team_list(self):
        """Execute team listing test"""
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)

        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

    def test_team_create(self):
        """Execute team create test"""
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)

        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request(),
                    variables={"team": {"description": "Isotopes","active": True}})
#                                       context=test_data.get_variables())
        print(executed)

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

if __name__ == '__main__':
    unittest.main()
