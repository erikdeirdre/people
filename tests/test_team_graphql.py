""" Unit Test Module for Graphql """
import sys
from os.path import (join, abspath, dirname)
from json import (loads, dumps)
import unittest
import pytest
from graphene.test import Client
from testhelper.testhelper import TestHelper
from app.schema import SCHEMA

TestHelper.__test__ = False


@pytest.mark.usefixtures("init_database")
class TestTeamGraphGL(unittest.TestCase):
    """Test Suite for testing Sport GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)
    last_id = None

    def test_team_list(self):
        """Execute team listing test"""
        test_data = TestHelper(self.dir_name,
                              sys._getframe(  ).f_code.co_name)

        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])

    def test_team_create(self):
        """Execute team create test"""
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
