# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models


class CountryDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:country_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_country()

    def test_anonymous_user(self):
        self.do_test()


class CountryListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:country_list'

    def test_anonymous_user(self):
        '''Anyone should be able to access a list of all the countries.'''
        country1 = models.new_country(name='USA')
        country2 = models.new_country(name='China')
        country3 = models.new_country(name='Barbara Boxer', special=True)

        response = self.get_response()
        self.assertEqual(response.data, [
            {'id': country1.id,
             'special': country1.special,
             'name': country1.name},
            {'id': country2.id,
             'special': country2.special,
             'name': country2.name},
            {'id': country3.id,
             'special': country3.special,
             'name': country3.name}])


class CountryDetailDeleteTestCase(auto.DestroyAPIAutoTestCase):
    url_name = 'api:country_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_country()

    def test_anonymous_user(self):
        '''Anonymous users cannot delete countries.'''
        self.do_test(expected_error=auto.EXP_DELETE_NOT_ALLOWED)

    def test_authenticated_user(self):
        '''Authenticated users cannot delete countries.'''
        self.as_default_user().do_test(expected_error=auto.EXP_DELETE_NOT_ALLOWED)

    def test_superuser(self):
        '''Superusers cannot delete countries.'''
        self.as_superuser().do_test(expected_error=auto.EXP_DELETE_NOT_ALLOWED)


class CountryDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:country_detail'
    params = {'name': 'Barbara Boxer',
              'special': True}

    def setUp(self):
        self.country = models.new_country(name='USA', special=False)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update countries.'''
        response = self.get_response(self.country.id, params=self.params)
        self.assertMethodNotAllowed(response, 'PATCH')

    def test_authenticated_user(self):
        '''Authenticated users shouldn't be able to update countries.'''
        models.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.country.id, params=self.params)
        self.assertMethodNotAllowed(response, 'PATCH')

    def test_superuser(self):
        '''Superusers shouldn't be able to update countries.'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.country.id, params=self.params)
        self.assertMethodNotAllowed(response, 'PATCH')


class CountryListPostTestCase(tests.CreateAPITestCase):
    url_name = 'api:country_list'
    params = {'name': 'USA',
              'special': False}

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to create countries.'''
        response = self.get_response(self.params)
        self.assertMethodNotAllowed(response, 'POST')

    def test_self(self):
        '''Authenticated users shouldn't be able to create countries.'''
        models.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.params)
        self.assertMethodNotAllowed(response, 'POST')

    def test_super_user(self):
        '''Superusers shouldn't be able to create countries.'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.params)
        self.assertMethodNotAllowed(response, 'POST')
