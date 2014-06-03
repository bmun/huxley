# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api.tests import (CreateAPITestCase, DestroyAPITestCase,
                              ListAPITestCase, PartialUpdateAPITestCase,
                              RetrieveAPITestCase)
from huxley.utils.test import TestCountries, TestUsers


class CountryDetailGetTestCase(RetrieveAPITestCase):
    url_name = 'api:country_detail'

    def test_anonymous_user(self):
        '''Fields should be returned when accessed by any user.'''
        country = TestCountries.new_country()
        response = self.get_response(country.id)
        self.assertEqual(response.data, {
            'id': country.id,
            'name': country.name,
            'special': country.special})


class CountryListGetTestCase(ListAPITestCase):
    url_name = 'api:country_list'

    def test_anonymous_user(self):
        '''Anyone should be able to access a list of all the countries.'''
        country1 = TestCountries.new_country(name='USA')
        country2 = TestCountries.new_country(name='China')
        country3 = TestCountries.new_country(name='Barbara Boxer', special=True)

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


class CountryDetailDeleteTestCase(DestroyAPITestCase):
    url_name = 'api:country_detail'

    def setUp(self):
        self.country = TestCountries.new_country()

    def test_anonymous_user(self):
        '''Unauthenticated users should not be able to delete countries.'''
        response = self.get_response(self.country.id)
        self.assertNotAuthenticated(response)

    def test_self(self):
        '''Authenticated users shouldn't have permission to delete countries.'''
        TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.country.id)
        self.assertPermissionDenied(response)

    def test_super_user(self):
        '''Countries should not be able to be deleted'''
        TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.country.id)
        self.assertMethodNotAllowed(response, 'DELETE')


class CountryDetailPatchTestCase(PartialUpdateAPITestCase):
    url_name = 'api:country_detail'
    params = {'name': 'Barbara Boxer',
              'special': True}

    def setUp(self):
        self.country = TestCountries.new_country(name='USA', special=False)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update countries.'''
        response = self.get_response(self.country.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_authenticated_user(self):
        '''Authenticated users shouldn't be able to update countries.'''
        TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.country.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''Superusers shouldn't be able to update countries.'''
        TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.country.id, params=self.params)
        self.assertMethodNotAllowed(response, 'PATCH')


class CountryListPostTestCase(CreateAPITestCase):
    url_name = 'api:country_list'
    params = {'name': 'USA',
              'special': False}

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to create countries.'''
        response = self.get_response(self.params)
        self.assertNotAuthenticated(response)

    def test_self(self):
        '''Authenticated users shouldn't be able to create countries.'''
        TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.params)
        self.assertPermissionDenied(response)

    def test_super_user(self):
        '''Superusers shouldn't be able to create countries.'''
        TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.params)
        self.assertMethodNotAllowed(response, 'POST')
