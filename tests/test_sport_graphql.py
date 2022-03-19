""" Unit Test Module for Graphql """
from cgi import test
import sys
from os.path import (join, abspath, dirname)
import unittest
import pytest
from graphene.test import Client
from app.schema import SCHEMA
from .helpers.load_data import get_test_data


@pytest.mark.usefixtures("init_database")
class TestSportGraphGL(unittest.TestCase):
    """Test Suite for testing Sport GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)

    @pytest.mark.order(1)
    def test_sport_list(self):
        """Execute sport listing test"""
        test_data = get_test_data(self.dir_name,
                                  sys._getframe(  ).f_code.co_name)
        executed = self.client.execute(test_data.get_send_request())

        self.assertDictEqual(executed['data'],
                             test_data.get_expected_result()['data'])

    @pytest.mark.order(2)
    def test_sport_create(self):
        """Execute sport create test"""
        test_data = get_test_data(self.dir_name,
                                  sys._getframe(  ).f_code.co_name)

        executed = self.client.execute(
            test_data.get_send_request(),
            variable_values=test_data.get_variables())

        self.assertDictEqual(executed['data'],
                             test_data.get_expected_result()['data'])

if __name__ == '__main__':
    unittest.main()
