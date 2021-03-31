""" Unit Test Module for Graphql """
import sys
from os.path import (join, abspath, dirname)
from glob import glob
from json import (loads, dumps)
import unittest
import pytest
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
from graphene.test import Client
from testclass.testclass import TestClass
from app import DB
from app.schema import SCHEMA

@pytest.mark.usefixtures("init_database")
class TestCoachGraphGL(unittest.TestCase):
    """Test Suite for testing Coach GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)

    def test_coach_list(self):
        """Execute coach query test"""
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        print(dumps(executed['data']))
        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])


if __name__ == '__main__':
    unittest.main()
