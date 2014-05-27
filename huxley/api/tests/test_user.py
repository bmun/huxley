# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.accounts.models import HuxleyUser
from huxley.api.tests import (CreateAPITestCase, DestroyAPITestCase,
                              ListAPITestCase, PartialUpdateAPITestCase,
                              RetrieveAPITestCase)
from huxley.utils.test import TestUsers


class UserDetailGetTestCase(RetrieveAPITestCase):
    url_name = 'api:user_detail'

    def test_anonymous_user(self):
        '''It should reject request from an anonymous user.'''
        user = TestUsers.new_user()
        response = self.get_response(user.id)

        self.assertEqual(response.data, {
            'detail': u'Authentication credentials were not provided.'})

    def test_other_user(self):
        '''It should reject request from another user.'''
        user1 = TestUsers.new_user(username='user1')
        user2 = TestUsers.new_user(username='user2', password='user2')

        self.client.login(username='user2', password='user2')
        response = self.get_response(user1.id)

        self.assertEqual(response.data, {
            'detail': u'You do not have permission to perform this action.'})

    def test_superuser(self):
        '''It should return the correct fields for a superuser.'''
        user1 = TestUsers.new_user(username='user1')
        user2 = TestUsers.new_superuser(username='user2', password='user2')

        self.client.login(username='user2', password='user2')
        response = self.get_response(user1.id)

        self.assertEqual(response.data, {
            'id': user1.id,
            'username': user1.username,
            'first_name': user1.first_name,
            'last_name': user1.last_name,
            'user_type': user1.user_type,
            'school': user1.school_id,
            'committee': user1.committee_id})

    def test_self(self):
        '''It should return the correct fields for a single user.'''
        user = TestUsers.new_user(username='lol', password='lol', school_id=1)
        self.client.login(username='lol', password='lol')
        response = self.get_response(user.id)

        self.assertEqual(response.data, {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
            'school': user.school_id,
            'committee': user.committee_id})

    def test_chair(self):
        '''It should have the correct fields for chairs.'''
        user = TestUsers.new_user(user_type=HuxleyUser.TYPE_CHAIR,
                                  committee_id=4)
        self.client.login(username='testuser', password='test')
        response = self.get_response(user.id)

        self.assertEqual(response.data, {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
            'school': user.school_id,
            'committee': user.committee_id})


class UserDetailDeleteTestCase(DestroyAPITestCase):
    url_name = 'api:user_detail'

    def setUp(self):
        self.user = TestUsers.new_user(username='user1', password='user1')

    def test_anonymous_user(self):
        '''It should reject the request from an anonymous user.'''
        response = self.get_response(self.user.id)

        self.assertEqual(response.data, {
            'detail': u'Authentication credentials were not provided.'})
        self.assertTrue(HuxleyUser.objects.filter(id=self.user.id).exists())

    def test_other_user(self):
        '''It should reject the request from another user.'''
        TestUsers.new_user(username='user2', password='user2')
        self.client.login(username='user2', password='user2')

        response = self.get_response(self.user.id)
        self.assertEqual(response.data, {
            'detail': u'You do not have permission to perform this action.'})
        self.assertTrue(HuxleyUser.objects.filter(id=self.user.id).exists())

    def test_self(self):
        '''It should allow a user to delete themself.'''
        self.client.login(username='user1', password='user1')

        response = self.get_response(self.user.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(HuxleyUser.objects.filter(id=self.user.id).exists())

    def test_superuser(self):
        '''It should allow a superuser to delete a user.'''
        TestUsers.new_superuser(username='user2', password='user2')
        self.client.login(username='user2', password='user2')

        response = self.get_response(self.user.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(HuxleyUser.objects.filter(id=self.user.id).exists())


class UserDetailPatchTestCase(PartialUpdateAPITestCase):
    url_name = 'api:user_detail'
    params = {'first_name': 'first',
              'last_name': 'last'}

    def setUp(self):
        self.user = TestUsers.new_user(username='user1', password='user1')

    def test_anonymous_user(self):
        '''An anonymous user should not be able to change information.'''
        response = self.get_response(self.user.id, params=self.params)
        self.assertEqual(response.data, {
            'detail': u'Authentication credentials were not provided.'})

        user = HuxleyUser.objects.get(id=self.user.id)
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

    def test_other_user(self):
        '''Another user should not be able to change information about any other user.'''
        TestUsers.new_user(username='user2', password='user2')
        self.client.login(username='user2', password='user2')

        response = self.get_response(self.user.id, params=self.params)
        self.assertEqual(response.data, {
            'detail': u'You do not have permission to perform this action.'})

        user = HuxleyUser.objects.get(id=self.user.id)
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

    def test_self(self):
        '''A User should be allowed to change information about himself.'''
        self.client.login(username='user1', password='user1')

        response = self.get_response(self.user.id, params=self.params)
        user = HuxleyUser.objects.get(id=self.user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)

    def test_superuser(self):
        '''A superuser should be allowed to change information about a user.'''
        TestUsers.new_superuser(username='user2', password='user2')
        self.client.login(username='user2', password='user2')

        response = self.get_response(self.user.id, params=self.params)
        user = HuxleyUser.objects.get(id=self.user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)


class UserListGetTestCase(ListAPITestCase):
    url_name = 'api:user_list'

    def test_anonymous_user(self):
        '''It should reject the request from an anonymous user.'''
        TestUsers.new_user(username='user1')
        TestUsers.new_user(username='user2')

        response = self.get_response()
        self.assertEqual(response.data, {
            'detail': u'Authentication credentials were not provided.'})

    def test_user(self):
        '''It should reject the request from a regular user.'''
        TestUsers.new_user(username='user1', password='user1')
        TestUsers.new_user(username='user2')
        self.client.login(username='user1', password='user1')

        response = self.get_response()
        self.assertEqual(response.data, {
            'detail': u'You do not have permission to perform this action.'})

    def test_superuser(self):
        '''It should allow a superuser to list all users.'''
        user1 = TestUsers.new_superuser(username='user1', password='user1')
        user2 = TestUsers.new_user(username='user2')
        self.client.login(username='user1', password='user1')

        response = self.get_response()
        self.assertEqual(response.data, [
            {'id': user1.id,
             'username': user1.username,
             'first_name': user1.first_name,
             'last_name': user1.last_name,
             'user_type': user1.user_type,
             'school': user1.school_id,
             'committee': user1.committee_id},
            {'id': user2.id,
             'username': user2.username,
             'first_name': user2.first_name,
             'last_name': user2.last_name,
             'user_type': user2.user_type,
             'school': user2.school_id,
             'committee': user2.committee_id}])


class UserListPostTestCase(CreateAPITestCase):
    url_name = 'api:user_list'
    params = {'username': 'Kunal',
              'password': 'pass',
              'first_name': 'Kunal',
              'last_name': 'Mehta'}

    def test_valid(self):
        params = self.get_params()
        response = self.get_response(params)

        user_query = HuxleyUser.objects.filter(id=response.data['id'])
        self.assertTrue(user_query.exists())

        user = HuxleyUser.objects.get(id=response.data['id'])
        self.assertEqual(response.data, {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': HuxleyUser.TYPE_ADVISOR,
            'school': user.school_id})

    def test_empty_username(self):
        response = self.get_response(params=self.get_params(username=''))
        self.assertEqual(response.data, {
            'username': ['This field is required.']})

    def test_taken_username(self):
        TestUsers.new_user(username='_Kunal', password='pass')
        response = self.get_response(params=self.get_params(username='_Kunal'))
        self.assertEqual(response.data, {
            'username': ['This username is already taken.']})

    def test_invalid_username(self):
        response = self.get_response(params=self.get_params(username='>Kunal'))
        self.assertEqual(response.data, {
            'username': ['Usernames may contain alphanumerics, underscores, '
                         'and/or hyphens only.']})

    def test_empty_password(self):
        response = self.get_response(params=self.get_params(password=''))
        self.assertEqual(response.data, {
            'password': ['This field is required.']})

    def test_invalid_password(self):
        response = self.get_response(params=self.get_params(password='>pass'))
        self.assertEqual(response.data, {
            'password': ['Password contains invalid characters.']})


class CurrentUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:current_user')

    def get_data(self, url):
        return json.loads(self.client.get(url).content)

    def test_login(self):
        user = TestUsers.new_user(username='lol', password='lol')
        user2 = TestUsers.new_user(username='bunny', password='bunny')

        credentials = {'username': 'lol', 'password': 'lol'}
        response = self.client.post(self.url,
                                    data=json.dumps(credentials),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.session['_auth_user_id'], user.id)


        credentials = {'username': 'bunny', 'password': 'bunny'}
        response = self.client.post(self.url,
                                    data=json.dumps(credentials),
                                    content_type='application/json')
        self.assertEqual(self.client.session['_auth_user_id'], user.id)

        data = json.loads(response.content)
        self.assertEqual(data['detail'],
                         'Another user is currently logged in.')

    def test_logout(self):
        user = TestUsers.new_user(username='lol', password='lol')

        self.client.login(username='lol', password='lol')
        self.assertEqual(self.client.session['_auth_user_id'], user.id)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertTrue('_auth_user_id' not in self.client.session)

    def test_get(self):
        data = self.get_data(self.url)

        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'], 'Not found')

        user = TestUsers.new_user(username='lol', password='lol', school_id=1)
        self.client.login(username='lol', password='lol')

        data = self.get_data(self.url)
        self.assertEqual(len(data.keys()), 7)
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['username'], user.username)
        self.assertEqual(data['first_name'], user.first_name)
        self.assertEqual(data['last_name'], user.last_name)
        self.assertEqual(data['user_type'], HuxleyUser.TYPE_ADVISOR)
        self.assertEqual(data['school'], user.school_id)

