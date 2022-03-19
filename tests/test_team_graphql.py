""" Unit Test Module for Graphql """
import sys
from os.path import (join, abspath, dirname)
import unittest
import pytest
from graphene.test import Client
from .helpers.load_data import get_test_data
from app.schema import SCHEMA


@pytest.mark.usefixtures("init_database")
class TestTeamGraphGL(unittest.TestCase):
    """Test Suite for testing Sport GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)
    last_id = None

    @pytest.mark.order(1)
    def test_team_list(self):
        """Execute team listing test"""
        test_data = get_test_data(self.dir_name,
                                  sys._getframe(  ).f_code.co_name)

        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())
        self.assertDictEqual(executed['data'],
                             test_data.get_expected_result()['data'])

    @pytest.mark.order(2)
    def test_team_create(self):
        """Execute team create test"""
        test_data = get_test_data(self.dir_name,
                                  sys._getframe(  ).f_code.co_name)

        test_data.load_files()

        executed = self.client.execute(
            test_data.get_send_request(),
            variable_values=test_data.get_variables())

        self.assertDictEqual(executed['data'],
                             test_data.get_expected_result()['data'])

if __name__ == '__main__':
    unittest.main()
