""" Unit Test Module for Graphql """
import sys
from os.path import (join, abspath, dirname)
from json import (loads, dumps)
import unittest
import pytest
from graphene.test import Client
from app.schema import SCHEMA
from .helpers.load_data import get_test_data


@pytest.mark.usefixtures("init_database")
class TestAddressGraphGL(unittest.TestCase):
    """Test Suite for testing Address GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)

    def test_address(self):
        """Execute address test"""
        test_data = get_test_data(self.dir_name,
                                  sys._getframe(  ).f_code.co_name)

        executed = self.client.execute(test_data.get_send_request())

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])


    def test_citystate(self):
        """Execute city/state test"""
        test_data = get_test_data(self.dir_name,
                                  sys._getframe(  ).f_code.co_name)

        executed = self.client.execute(test_data.get_send_request())

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])


    def test_citystate_error(self):
        """Execute city/state error test"""
        test_data = get_test_data(self.dir_name,
                                  sys._getframe(  ).f_code.co_name)

        executed = self.client.execute(test_data.get_send_request())

        self.assertEqual(loads(dumps(executed['data'])),
                         test_data.get_expected_result()['data'])


if __name__ == '__main__':
    unittest.main()
