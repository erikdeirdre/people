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


def init_database():
    """Initializes the database """
    DB.drop_all()
    DB.create_all()

    base_dir = join(abspath(dirname(__file__)),  '..', '..')

    for fixture_file in glob(join(base_dir, 'seed', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)

    for fixture_file in glob(join(base_dir, 'seed', 'demo', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)


class TestSportGraphGL(unittest.TestCase):
    """Test Suite for testing Sport GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(schema)

    def setUp(self):
        """Initialize the database"""
        init_database()

    def test_sport_list(self):
        """Execute sport listing test"""
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)

        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])


if __name__ == '__main__':
    unittest.main()
