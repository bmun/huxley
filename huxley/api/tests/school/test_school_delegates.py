# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.exceptions import ValidationError

from huxley.api.tests import ListAPITestCase, PartialUpdateAPITestCase
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
            committee=self.committee1,
            country=self.country,
            school=self.school, )
        self.assignment2 = TestAssignments.new_assignment(
            committee=self.committee2,
            country=self.country,
            school=self.school, )
        self.delegate1 = TestDelegates.new_delegate(
            assignment=self.assignment1, )
        self.delegate2 = TestDelegates.new_delegate(
            assignment=self.assignment2,
            name='Trevor Dowds',
            email='t@dowds.com',
            summary='Good!')

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response(self.school.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It returns the delegates for the school's advisor.'''
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
        '''It returns the delegates for a superuser.'''
        TestUsers.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response(self.school.id)
        self.assert_delegate_equal(response)

    def assert_delegate_equal(self, response):
        '''Assert that the response contains the delegates in order.'''
        response.data[0].pop('created_at')
        response.data[1].pop('created_at')
        self.assertEqual(
            dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.assignment1.id,
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'session_one': False,
                'session_two': False,
                'session_three': False,
                'session_four': False,
            }, )
        self.assertEqual(
            dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.assignment2.id,
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
                'session_one': False,
                'session_two': False,
                'session_three': False,
                'session_four': False,
            }, )


class SchoolDelegateListPartialUpdateTestCase(PartialUpdateAPITestCase):
    url_name = 'api:school_delegates'

    def setUp(self):
        self.user = TestUsers.new_user(username='regular', password='user')
        self.school = TestSchools.new_school(user=self.user)

        self.country = TestCountries.new_country()
        self.committee1 = TestCommittees.new_committee()
        self.committee2 = TestCommittees.new_committee()
        self.committee3 = TestCommittees.new_committee()
        self.committee4 = TestCommittees.new_committee()

        self.assignment1 = TestAssignments.new_assignment(
            school=self.school, country=self.country, commitee=self.committee3)

        self.assignment2 = TestAssignments.new_assignment(
            school=self.school,
            country=self.country,
            committee=self.committee2)

        self.new_assignment = TestAssignments.new_assignment(
            school=self.school,
            country=self.country,
            committee=self.committee3)

        self.faulty_assignment = TestAssignments.new_assignment(
            country=self.country, committee=self.committee4)

        self.delegate1 = TestDelegates.new_delegate(
            name="Nathaniel Parke",
            school=self.school,
            assignment=self.assignment1)

        self.delegate2 = TestDelegates.new_delegate(
            name='Trevor Dowds',
            school=self.school,
            assignment=self.assignment2)

        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.new_assignment.id}, {'id': self.delegate2.id,
                                                     'assignment': None}
        ]

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response(self.school.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It updates the delegates for the school's advisor.'''
        self.client.login(username='regular', password='user')

        response = self.get_response(self.school.id)
        self.assertEqual(
            dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.params[0]['assignment'],
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'created_at': self.delegate1.created_at.isoformat(),
                'session_one': False,
                'session_two': False,
                'session_three': False,
                'session_four': False,
            }, )
        self.assertEqual(
            dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.params[1]['assignment'],
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
                'created_at': self.delegate2.created_at.isoformat(),
                'session_one': False,
                'session_two': False,
                'session_three': False,
                'session_four': False,
            }, )

    def test_advisor_fail(self):
        '''
        It doesn't update the delegates for the school's advisor if fields
        are invalid.
        '''
        self.client.login(username='regular', password='user')
        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.faulty_assignment.id},
            {'id': self.delegate2.id,
             'assignment': self.new_assignment.id}
        ]

        self.assertRaises(ValidationError, self.get_response, self.school.id)

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = TestUsers.new_user(username='another', password='user')
        TestSchools.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response(self.school.id)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It updates the delegates for a superuser.'''
        TestUsers.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response(self.school.id)
        self.assertEqual(
            dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.params[0]['assignment'],
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'created_at': self.delegate1.created_at.isoformat(),
                'session_one': False,
                'session_two': False,
                'session_three': False,
                'session_four': False,
            }, )
        self.assertEqual(
            dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.params[1]['assignment'],
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
                'created_at': self.delegate2.created_at.isoformat(),
                'session_one': False,
                'session_two': False,
                'session_three': False,
                'session_four': False,
            }, )

    def test_superuser_fail(self):
        '''
        It doesn't update the delegates for the superuser if fields are invalid.
        '''
        self.client.login(username='regular', password='user')
        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.faulty_assignment.id},
            {'id': self.delegate2.id,
             'assignment': self.new_assignment.id}
        ]

        self.assertRaises(ValidationError, self.get_response, self.school.id)
