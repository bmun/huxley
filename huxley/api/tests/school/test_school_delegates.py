# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api.tests import ListAPITestCase, UpdateAPITestCase
from huxley.core.models import Assignment, Delegate, School
from huxley.utils.test import (TestCommittees, TestCountries, TestSchools,
                               TestUsers, TestAssignments, TestDelegates)


class SchoolDelegateGetTestCase(ListAPITestCase):
    url_name = 'api:school_delegates'
    is_resource = True

    def setUp(self):
        self.user = TestUsers.new_user(username='regular', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.country = TestCountries.new_country()
        self.committee1 = TestCommittees.new_committee()
        self.committee2 = TestCommittees.new_committee()
        self.assignment1 = TestAssignments.new_assignment(
            committee=self.committee1.id,
            country=self.country.id,
            school=self.school.id,
        )
        self.assignment2 = TestAssignments.new_assignment(
            committee=self.committee2.id,
            country=self.country.id,
            school=self.school.id,
        )
        self.delegate1 = TestDelegates.new_delegate(
            assignment=self.assignment1.id,
        )
        self.delegate2 = TestDelegates.new_delegate(
            assignment=self.assignment2.id,
            name='Trevor Dowds',
            email='t@dowds.com',
            summary='Good!'
        )

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response(self.school.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It returns the assignments for the school's advisor.'''
        self.client.login(username='regular', password='user')

        response = self.get_response(self.school.id)
        self.assert_delegate_equal(response)

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = TestUsers.new_user(username='another', password='user')
        TestSchools.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response(self.school.id)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It returns the assignments for a superuser.'''
        TestUsers.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response(self.school.id)
        self.assert_delegate_equal(response)

    def assert_delegate_equal(self, response):
        '''Assert that the response contains the assignments in order.'''
        response.data[0].pop('created_at')
        response.data[1].pop('created_at')
        self.assertEqual(dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment':self.assignment1.id,
                'name':unicode(self.delegate1.name),
                'email':unicode(self.delegate1.email),
                'summary':unicode(self.delegate1.summary),
            },
        )
        self.assertEqual(dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment':self.assignment2.id,
                'name':unicode(self.delegate2.name),
                'email':unicode(self.delegate2.email),
                'summary':unicode(self.delegate2.summary),
            },
        )
