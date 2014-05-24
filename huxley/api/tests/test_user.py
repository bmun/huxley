# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.accounts.models import HuxleyUser
from huxley.api.tests import GetAPITestCase
from huxley.utils.test import TestSchools, TestUsers


class UserDetailGetTestCase(GetAPITestCase):
    url_name = 'api:user_detail'

    def test_anonymous_user(self):
        '''It should reject request from an anonymous user.'''
        user = TestUsers.new_user()
        data = self.get_response(user.id)

        self.assertEqual(data, {
            'detail': u'Authentication credentials were not provided.'})

    def test_other_user(self):
        '''It should reject request from another user.'''
        user1 = TestUsers.new_user(username='user1')
        user2 = TestUsers.new_user(username='user2', password='user2')

        self.client.login(username='user2', password='user2')
        data = self.get_response(user1.id)

        self.assertEqual(data, {
            'detail': u'You do not have permission to perform this action.'})

    def test_superuser(self):
        '''It should return the correct fields for a superuser.'''
        user1 = TestUsers.new_user(username='user1')
        user2 = TestUsers.new_superuser(username='user2', password='user2')

        self.client.login(username='user2', password='user2')
        data = self.get_response(user1.id)

        self.assertEqual(data, {
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
        data = self.get_response(user.id)

        self.assertEqual(data, {
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
        data = self.get_response(user.id)

        self.assertEqual(data, {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
            'school': user.school_id,
            'committee': user.committee_id})


class UserDetailDeleteTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, user_id):
        return reverse('api:user_detail', args=(user_id,))

    def get_response(self, url):
        return self.client.delete(url)

    def get_data(self, url):
        return json.loads(self.get_response(url).content)

    def test_anonymous_user(self):
        '''It should reject the request from an anonymous user.'''
        user = TestUsers.new_user()
        url = self.get_url(user.id)
        data = self.get_data(url)

        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'],
                         u'Authentication credentials were not provided.')
        self.assertTrue(HuxleyUser.objects.filter(id=user.id).exists())

    def test_other_user(self):
        '''It should reject the request from another user.'''
        username = 'user1'
        user1 = TestUsers.new_user(username=username)
        user2 = TestUsers.new_user(username='user2', password='user2')
        url = self.get_url(user1.id)

        self.client.login(username='user2', password='user2')
        data = self.get_data(url)

        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'],
                         u'You do not have permission to perform this action.')
        self.assertTrue(HuxleyUser.objects.filter(id=user1.id).exists())

    def test_self(self):
        '''It should allow a user to delete themself.'''
        user = TestUsers.new_user(username='lol', password='lol', school_id=1)
        url = self.get_url(user.id)

        self.client.login(username='lol', password='lol')
        response = self.get_response(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(HuxleyUser.objects.filter(id=user.id).exists())

    def test_superuser(self):
        '''It should allow a superuser to delete a user.'''
        user1 = TestUsers.new_user(username='user1')
        user2 = TestUsers.new_superuser(username='user2', password='user2')
        url = self.get_url(user1.id)

        self.client.login(username='user2', password='user2')
        response = self.get_response(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(HuxleyUser.objects.filter(id=user1.id).exists())


class UserDetailPatchTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, user_id):
        return reverse('api:user_detail', args=(user_id,))

    def get_data(self, url):
        return json.loads(self.client.get(url).content)

    def get_patch_response(self, url, data):
        response = self.client.patch(url, data=data, content_type='application/json')
        return json.loads(response.content)

    def test_anonymous_user(self):
        '''An anonymous user should not be able to change information.'''
        school = TestSchools.new_school()
        user = school.advisor
        url = self.get_url(user.id)
        fields = {'first_name': 'first',
                  'last_name': 'last'}

        response = self.get_patch_response(url, json.dumps(fields))
        data = self.get_data(url)

        self.assertEqual(len(response.keys()), 1)
        self.assertEqual(response['detail'],
            u'Authentication credentials were not provided.')
        self.assertTrue(HuxleyUser.objects.filter(id=user.id).exists())
        user = HuxleyUser.objects.get(id=user.id)
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

    def test_other_user(self):
        '''Another user should not be able to change information about any other user.'''
        user1 = TestUsers.new_user(username='user1', password='user1')
        user2 = TestUsers.new_user(username='user2', password='user2')
        url = self.get_url(user1.id)

        self.client.login(username='user2', password='user2')
        fields = {'first_name': 'first',
                  'last_name': 'last'}

        response = self.get_patch_response(url, json.dumps(fields))

        self.assertEqual(len(response.keys()), 1)
        self.assertEqual(response['detail'],
            u'You do not have permission to perform this action.')
        self.assertTrue(HuxleyUser.objects.filter(id=user1.id).exists())
        user1 = HuxleyUser.objects.get(id=user1.id)
        self.assertEqual(user1.first_name, 'Test')
        self.assertEqual(user1.last_name, 'User')

    def test_self(self):
        '''A User should be allowed to change information about himself.'''
        school = TestSchools.new_school()
        user = school.advisor
        url = self.get_url(user.id)

        self.client.login(username='testuser', password='test')
        data = self.get_data(url)

        fields = {'first_name': 'first',
                  'last_name': 'last'}

        response = self.get_patch_response(url, json.dumps(fields))
        user = HuxleyUser.objects.get(id=user.id)

        self.assertEqual(response['first_name'], user.first_name)
        self.assertEqual(response['last_name'], user.last_name)

    def test_superuser(self):
        '''A superuser should be allowed to change information about a user.'''
        school = TestSchools.new_school()
        user1 = school.advisor
        user2 = TestUsers.new_superuser(username='user2', password='user2')
        url = self.get_url(user1.id)

        self.client.login(username='user2', password='user2')

        fields = {'first_name': 'first',
                  'last_name': 'last'}

        response = self.get_patch_response(url, json.dumps(fields))
        user1 = HuxleyUser.objects.get(id=user1.id)

        self.assertEqual(response['first_name'], user1.first_name)
        self.assertEqual(response['last_name'], user1.last_name)


class UserListGetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:user_list')

    def get_data(self):
        return json.loads(self.client.get(self.url).content)

    def test_anonymous_user(self):
        '''It should reject the request from an anonymous user.'''
        TestUsers.new_user(username='user1')
        TestUsers.new_user(username='user2')

        data = self.get_data()
        self.assertTrue(type(data) is dict)
        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'],
                         u'Authentication credentials were not provided.')

    def test_user(self):
        '''It should reject the request from a regular user.'''
        TestUsers.new_user(username='user1', password='user1')
        TestUsers.new_user(username='user2')

        self.client.login(username='user1', password='user1')
        data = self.get_data()
        self.assertTrue(type(data) is dict)
        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'],
                         u'You do not have permission to perform this action.')

    def test_superuser(self):
        '''It should allow a superuser to list all users.'''
        user1 = TestUsers.new_superuser(username='user1', password='user1')
        user2 = TestUsers.new_user(username='user2')

        self.client.login(username='user1', password='user1')
        data = self.get_data()
        self.assertTrue(type(data) is list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0],
                         {'id': user1.id,
                          'username': user1.username,
                          'first_name': user1.first_name,
                          'last_name': user1.last_name,
                          'user_type': user1.user_type,
                          'school': user1.school_id,
                          'committee': user1.committee_id})
        self.assertEqual(data[1],
                         {'id': user2.id,
                          'username': user2.username,
                          'first_name': user2.first_name,
                          'last_name': user2.last_name,
                          'user_type': user2.user_type,
                          'school': user2.school_id,
                          'committee': user2.committee_id})


class UserListPostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:user_list')
        self.params = {'username': 'Kunal',
                       'password': 'pass',
                       'first_name': 'Kunal',
                       'last_name': 'Mehta'}

    def get_params(self, **kwargs):
        params = self.params.copy()
        for param, value in kwargs.items():
            params[param] = value
        return params

    def do_post(self, data):
        return self.client.post(self.url, json.dumps(data),
                                content_type='application/json')

    def get_response(self, data):
        return json.loads(self.do_post(data).content)

    def test_valid(self):
        params = self.get_params()
        response = self.get_response(params)
        self.assertTrue(HuxleyUser.objects.filter(id=response['id']).exists())

        user = HuxleyUser.objects.get(id=response['id'])
        self.assertEqual(len(response.keys()), 6)
        self.assertEqual(response['id'], user.id)
        self.assertEqual(response['username'], user.username)
        self.assertEqual(response['first_name'], user.first_name)
        self.assertEqual(response['last_name'], user.last_name)
        self.assertEqual(response['user_type'], HuxleyUser.TYPE_ADVISOR)
        self.assertEqual(response['school'], user.school_id)

    def test_empty_username(self):
        response = self.get_response(self.get_params(username=''))
        self.assertEqual(len(response.keys()), 1)
        self.assertEqual(response['username'],
                        ['This field is required.'])

    def test_taken_username(self):
        TestUsers.new_user(username='_Kunal', password='pass')
        response = self.get_response(self.get_params(username='_Kunal'))
        self.assertEqual(len(response.keys()), 1)
        self.assertEqual(response['username'],
                        ['This username is already taken.'])

    def test_invalid_username(self):
        response = self.get_response(self.get_params(username='>Kunal'))
        self.assertEqual(len(response.keys()), 1)
        self.assertEqual(response['username'],
                        ['Usernames may contain alphanumerics, underscores, '
                         'and/or hyphens only.'])

    def test_empty_password(self):
        response = self.get_response(self.get_params(password=''))
        self.assertEqual(len(response.keys()), 1)
        self.assertEqual(response['password'],
                        ['This field is required.'])

    def test_invalid_password(self):
        response = self.get_response(self.get_params(password='>pass'))
        self.assertEqual(len(response.keys()), 1)
        self.assertEqual(response['password'],
                        ['Password contains invalid characters.'])


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

