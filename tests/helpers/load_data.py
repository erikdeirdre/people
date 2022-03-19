from testhelper.testhelper import TestHelper

TestHelper.__test__ = False


def get_test_data(dir_name, test_name):
    test_data = TestHelper(dir_name, test_name)
    test_data.load_files()
    return test_data
