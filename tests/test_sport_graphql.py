""" Unit Test Module for Graphql """
import sys
from os.path import (join, abspath, dirname)
from json import (loads, dumps)
import unittest
import pytest
from graphene.test import Client
from testhelper.testhelper import TestHelper
from app.schema import SCHEMA

@pytest.mark.usefixtures("init_database")
class TestSportGraphGL(unittest.TestCase):
    """Test Suite for testing Sport GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)

    def test_sport_list(self):
        """Execute sport listing test"""
        test_data = TestHelper(self.dir_name,
                              sys._getframe(  ).f_code.co_name)

        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

    def test_sport_create(self):
        """Execute sport create test"""
        test_data = TestHelper(self.dir_name,
                              sys._getframe(  ).f_code.co_name)

        test_data.load_files()

        executed = self.client.execute(
            test_data.get_send_request(),
            variables=test_data.get_variables())

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

if __name__ == '__main__':
    unittest.main()
