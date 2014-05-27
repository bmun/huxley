# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api.tests import (CreateAPITestCase, DestroyAPITestCase,
                              ListAPITestCase, PartialUpdateAPITestCase,
                              RetrieveAPITestCase, UpdateAPITestCase)
from huxley.utils.test import TestCommittees, TestUsers


class CommitteeDetailGetTestCase(RetrieveAPITestCase):
    url_name = 'api:committee_detail'

    def test_anonymous_user(self):
        '''It should return the correct fields for a committee.'''
        c = TestCommittees.new_committee()
        response = self.get_response(c.id)
        self.assertEqual(response.data, {
            'id': c.id,
            'name': c.name,
            'full_name': c.full_name,
            'delegation_size': c.delegation_size,
            'special': c.special})


class CommitteeDetailPutTestCase(UpdateAPITestCase):
    url_name = 'api:committee_detail'
    params = {'name':'DISC',
              'special':True}

    def setUp(self):
        self.committee = TestCommittees.new_committee()

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update committees.'''
        response = self.get_response(self.committee.id, params=self.params)
        self.assertEqual(response.data, {
            'detail': u'Authentication credentials were not provided.'})

    def test_authenticated_user(self):
        '''Authenticated users shouldn't be able to update committees.'''
        TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        self.assertEqual(response.data, {
            'detail': u'You do not have permission to perform this action.'})

    def test_superuser(self):
        '''Superusers shouldn't be able to update committees.'''
        TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        self.assertEqual(response.data, {
            'detail': u"Method 'PUT' not allowed."})


class CommitteeDetailPatchTestCase(PartialUpdateAPITestCase):
    url_name = 'api:committee_detail'
    params = {'name':'DISC',
              'special':True}

    def setUp(self):
        self.committee = TestCommittees.new_committee()

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update committees.'''
        response = self.get_response(self.committee.id, params=self.params)
        self.assertEqual(response.data, {
            'detail': u'Authentication credentials were not provided.'})

    def test_authenticated_user(self):
        '''Authenticated users shouldn't be able to update committees.'''
        TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        self.assertEqual(response.data, {
            'detail': u'You do not have permission to perform this action.'})

    def test_superuser(self):
        '''Superusers shouldn't be able to update committees.'''
        TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.committee.id, params=self.params)
        self.assertEqual(response.data, {
            'detail': u"Method 'PATCH' not allowed."})


class CommitteeDetailDeleteTestCase(DestroyAPITestCase):
    url_name = 'api:committee_detail'

    def setUp(self):
        self.committee = TestCommittees.new_committee()

    def test_anonymous_user(self):
        '''Unauthenticated users should not be able to delete committees.'''
        response = self.get_response(self.committee.id)
        self.assertEqual(response.data, {
            'detail':  u'Authentication credentials were not provided.'})

    def test_self(self):
        '''Authenticated users shouldn't have permission to delete committees.'''
        TestUsers.new_user(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.committee.id)
        self.assertEqual(response.data, {
            'detail':  u'You do not have permission to perform this action.'})

    def test_super_user(self):
        '''Countries should not be able to be deleted'''
        TestUsers.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')

        response = self.get_response(self.committee.id)
        self.assertEqual(response.data, {
            'detail':  u"Method 'DELETE' not allowed."})


class CommitteeListGetTestCase(ListAPITestCase):
    url_name = 'api:committee_list'

    def test_anonymous_user(self):
        '''Anyone should be able to access a list of all the committees.'''
        c1 = TestCommittees.new_committee(name='DISC', delegation_size=100)
        c2 = TestCommittees.new_committee(name='JCC', special=True,
                                          delegation_size=30)

        response = self.get_response()
        self.assertEqual(response.data, [
            {'delegation_size': c1.delegation_size,
             'special': c1.special,
             'id': c1.id,
             'full_name': c1.full_name,
             'name': c1.name},
            {'delegation_size': c2.delegation_size,
             'special': c2.special,
             'id': c2.id,
             'full_name': c2.full_name,
             'name': c2.name}])


class CommitteeListPostTestCase(CreateAPITestCase):
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
