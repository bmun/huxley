# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.api.tests import GetAPITestCase, PostAPITestCase
from huxley.utils.test import TestCommittees, TestUsers


class CommitteeDetailGetTestCase(GetAPITestCase):
    url_name = 'api:committee_detail'

    def test_anonymous_user(self):
        '''It should return the correct fields for a committee.'''
        c = TestCommittees.new_committee()

        data = self.get_response(c.id)
        self.assertEqual(data, {'id': c.id,
                                'name': c.name,
                                'full_name': c.full_name,
                                'delegation_size': c.delegation_size,
                                'special': c.special})


class CommitteeDetailPutTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.committee = TestCommittees.new_committee()
        self.url = reverse('api:committee_detail', args=(self.committee.id,))
        self.params = {'name':'DISC',
                       'special':True}

    def get_response(self, data):
        return json.loads(self.client.put(self.url, data=data,
            content_type='application/json').content)

    def test_anonymous_user(self):
        '''Unauthenticated users should not be able to update committees.'''
        response = self.get_response(self.params)
        self.assertEqual(response['detail'],
                            u'Authentication credentials were not provided.')

    def test_self(self):
        '''Authenticated users shouldn't have permission to update committees.'''
        user = TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response(self.params)
        self.assertEqual(response['detail'],
            'You do not have permission to perform this action.')

    def test_super_user(self):
        '''Committees should not be able to be updated.'''
        user = TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response(self.params)
        self.assertEqual(response['detail'], "Method 'PUT' not allowed.")


class CommitteeDetailPatchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.committee = TestCommittees.new_committee()
        self.url = reverse('api:committee_detail', args=(self.committee.id,))
        self.params = {'name':'DISC',
                       'special':True}

    def get_response(self, data):
        return json.loads(self.client.patch(self.url, data=data,
            content_type='application/json').content)

    def test_anonymous_user(self):
        '''Unauthenticated users should not be able to update committees.'''
        response = self.get_response(self.params)
        self.assertEqual(response['detail'],
                            u'Authentication credentials were not provided.')

    def test_self(self):
        '''Authenticated users shouldn't have permission to update committees.'''
        user = TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response(self.params)
        self.assertEqual(response['detail'],
            'You do not have permission to perform this action.')

    def test_super_user(self):
        '''Committees should not be able to be updated.'''
        user = TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response(self.params)
        self.assertEqual(response['detail'], "Method 'PATCH' not allowed.")


class CommitteeDetailDeleteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.committee = TestCommittees.new_committee()
        self.url = reverse('api:committee_detail', args=(self.committee.id,))

    def get_response(self):
        return json.loads(self.client.delete(self.url).content)

    def test_anonymous_user(self):
        '''Unauthenticated users should not be able to delete committees.'''
        response = self.get_response()
        self.assertEqual(response['detail'],
            'Authentication credentials were not provided.')

    def test_self(self):
        '''Authenticated users shouldn't have permission to delete committees.'''
        user = TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response()
        self.assertEqual(response['detail'],
            'You do not have permission to perform this action.')

    def test_super_user(self):
        '''Committees should not be able to be deleted.'''
        user = TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response()
        self.assertEqual(response['detail'], "Method 'DELETE' not allowed.")


class CommitteeListGetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:committee_list')

    def get_data(self):
        return json.loads(self.client.get(self.url).content)

    def test_anonymous_user(self):
        '''It should return the correct list of committees.
        Anyone can access committee list.'''
        c1 = TestCommittees.new_committee(name='DISC', delegation_size=100)
        c2 = TestCommittees.new_committee(name='JCC', special=True,
                                             delegation_size=30)

        data = self.get_data()
        self.assertTrue(type(data) is list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0],
                         {'delegation_size': c1.delegation_size,
                          'special': c1.special,
                          'id': c1.id,
                          'full_name': c1.full_name,
                          'name': c1.name})
        self.assertEqual(data[1],
                         {'delegation_size': c2.delegation_size,
                          'special': c2.special,
                          'id': c2.id,
                          'full_name': c2.full_name,
                          'name': c2.name})


class CommitteeListPostTestCase(PostAPITestCase):
    url_name = 'api:committee_list'
    params = {'name': 'DISC',
              'full_name': 'Disarmament and International Security',
              'delegation_size': 100}

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to create committees.'''
        response = self.get_response(self.params)
        self.assertEqual(response.data, {
            'detail': u'Authentication credentials were not provided.'})

    def test_authenticated_user(self):
        '''Authenticated users shouldn't be able to create committees.'''
        TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.params)
        self.assertEqual(response.data, {
            'detail': u'You do not have permission to perform this action.'})

    def test_superuser(self):
        '''Superusers shouldn't be able to create committees.'''
        TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.params)
        self.assertEqual(response.data, {
            'detail': u"Method 'POST' not allowed."})
