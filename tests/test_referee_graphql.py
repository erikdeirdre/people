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
class TestRefereeGraphGL(unittest.TestCase):
    """Test Suite for testing Referee GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)

    def test_referee_list(self):
        """Execute referee query test"""
        test_data = TestHelper(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        executed = self.client.execute(test_data.get_send_request())

        self.assertDictEqual(executed['data'],
                         test_data.get_expected_result()['data'])


if __name__ == '__main__':
    unittest.main()
