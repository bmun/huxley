# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.accounts.models import HuxleyUser
from huxley.utils.test import TestUsers


class UserDetailGetTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, user_id):
        return reverse('api:user_detail', args=(user_id,))

    def get_response(self, url):
        return json.loads(self.client.get(url).content)

    def test_anonymous_user(self):
        '''It should reject request from an anonymous user.'''
        user = TestUsers.new_user()
        url = self.get_url(user.id)
        data = self.get_response(url)

        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'],
                         u'Authentication credentials were not provided.')

    def test_other_user(self):
        '''It should reject request from another user.'''
        user1 = TestUsers.new_user(username='user1')
        user2 = TestUsers.new_user(username='user2', password='user2')
        url = self.get_url(user1.id)

        self.client.login(username='user2', password='user2')
        data = self.get_response(url)

        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'],
                         u'You do not have permission to perform this action.')

    def test_superuser(self):
        '''It should return the correct fields for a superuser.'''
        user1 = TestUsers.new_user(username='user1')
        user2 = TestUsers.new_superuser(username='user2', password='user2')
        url = self.get_url(user1.id)

        self.client.login(username='user2', password='user2')
        data = self.get_response(url)

        self.assertEqual(len(data.keys()), 6)
        self.assertEqual(data['id'], user1.id)
        self.assertEqual(data['first_name'], user1.first_name)
        self.assertEqual(data['last_name'], user1.last_name)
        self.assertEqual(data['user_type'], HuxleyUser.TYPE_ADVISOR)
        self.assertEqual(data['school'], user1.school_id)
        self.assertEqual(data['committee'], user1.committee_id)

    def test_self(self):
        '''It should return the correct fields for a single user.'''
        user = TestUsers.new_user(username='lol', password='lol', school_id=1)
        url = self.get_url(user.id)

        self.client.login(username='lol', password='lol')
        data = self.get_response(url)

        self.assertEqual(len(data.keys()), 6)
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['first_name'], user.first_name)
        self.assertEqual(data['last_name'], user.last_name)
        self.assertEqual(data['user_type'], HuxleyUser.TYPE_ADVISOR)
        self.assertEqual(data['school'], user.school_id)
        self.assertEqual(data['committee'], user.committee_id)

    def test_chair(self):
        '''It should have the correct fields for chairs.'''
        user = TestUsers.new_user(user_type=HuxleyUser.TYPE_CHAIR,
                                  committee_id=4)
        url = self.get_url(user.id)

        self.client.login(username='testuser', password='test')
        data = self.get_response(url)

        self.assertEqual(len(data.keys()), 6)
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['first_name'], user.first_name)
        self.assertEqual(data['last_name'], user.last_name)
        self.assertEqual(data['user_type'], HuxleyUser.TYPE_CHAIR)
        self.assertEqual(data['school'], user.school_id)
        self.assertEqual(data['committee'], user.committee_id)


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
        self.assertEqual(len(data.keys()), 6)
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['first_name'], user.first_name)
        self.assertEqual(data['last_name'], user.last_name)
        self.assertEqual(data['user_type'], HuxleyUser.TYPE_ADVISOR)
        self.assertEqual(data['school'], user.school_id)
