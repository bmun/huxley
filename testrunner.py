"""
    Courtesy of: http://stackoverflow.com/questions/5917587/django-unit-tests-without-a-db
"""

from django.test.simple import DjangoTestSuiteRunner

class NoDbTestRunner(DjangoTestSuiteRunner):
    """ A test runner that does not create/destroy a database """
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass