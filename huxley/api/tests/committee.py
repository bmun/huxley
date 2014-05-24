# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.utils.test import TestCommittees, TestUsers


class CommitteeDetailGetTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, committee_id):
        return reverse('api:committee_detail', args=(committee_id,))

    def get_response(self, url):
        return json.loads(self.client.get(url).content)

    def test_anonymous_user(self):
        '''It should return the correct fields for a committee.'''
        c = TestCommittees.new_committee()
        url = self.get_url(c.id)

        data = self.get_response(url)
        self.assertEqual(data['delegation_size'], c.delegation_size)
        self.assertEqual(data['special'], c.special)
        self.assertEqual(data['id'], c.id)
        self.assertEqual(data['full_name'], c.full_name)
        self.assertEqual(data['name'], c.name)


class CommitteeDetailPutTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, committee_id):
        return reverse('api:committee_detail', args=(committee_id,))

class CommitteeDetailPatchTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, committee_id):
        return reverse('api:committee_detail', args=(committee_id,))

class CommitteeDetailDeleteTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, committee_id):
        return reverse('api:committee_detail', args=(committee_id,))

class CommitteeListGetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("api:committee_list")

    def get_data(self):
        return json.loads(self.client.get(self.url).content)

    def test_anonymous_user(self):
        '''It should return the correct list of committees. Anyone can access committee list.'''
        c1 = TestCommittees.new_committee(name='DISC', delegation_size=100)
        c2 = TestCommittees.new_committee(name='JCC', special=True, delegation_size=30)


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



class CommitteeListPostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("api:committee_list")
        self.params = {'name': 'DISC',
                       'delegation_size': 100}

    def get_response(self, data):
        return json.loads(self.client.post(self.url, data=data,
                          content_type='application/json').content)

    def test_anonymous_user(self):
        '''Unauthenticated users should not be able to post.'''
        response = self.get_response(json.dumps(self.params))
        self.assertEqual(response['detail'],
            u'Authentication credentials were not provided.')

    def test_self(self):
        '''Authenticated users shouldn't be able to create committees.'''
        user= TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(json.dumps(self.params))
        self.assertEqual(response['detail'],
            u'You do not have permission to perform this action.')

    def test_superuser(self):
        '''Post action is not exposed to a superuser.'''
        user= TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(json.dumps(self.params))
        print(response)
        #self.assertEqual(response['detail'], "Method 'POST' not allowed.")
