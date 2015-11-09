# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api.tests import ListAPITestCase, UpdateAPITestCase
from huxley.core.models import Assignment, School
from huxley.utils.test import (TestCommittees, TestCountries, TestSchools,
                               TestUsers)


class SchoolAssignmentsGetTestCase(ListAPITestCase):
    url_name = 'api:school_assignments'
    is_resource = True

    def setUp(self):
        self.user = TestUsers.new_user(username='regular', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.country = TestCountries.new_country()
        self.committee1 = TestCommittees.new_committee()
        self.committee2 = TestCommittees.new_committee()
        self.assignment1 = Assignment.objects.create(
            committee=self.committee1,
            country=self.country,
            school=self.school,
        )
        self.assignment2 = Assignment.objects.create(
            committee=self.committee2,
            country=self.country,
            school=self.school,
        )

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response(self.school.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It returns the assignments for the school's advisor.'''
        self.client.login(username='regular', password='user')

        response = self.get_response(self.school.id)
        self.assert_assignments_equal(response)

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
        self.assert_assignments_equal(response)

    def assert_assignments_equal(self, response):
        '''Assert that the response contains the assignments in order.'''
        self.assertEqual(response.data, [
            {
                'id': self.assignment1.id,
                'country': self.country.id,
                'committee': self.committee1.id,
                'school': self.school.id,
            },
            {
                'id': self.assignment2.id,
                'country': self.country.id,
                'committee': self.committee2.id,
                'school': self.school.id,
            },
        ])

class SchoolAssignmentsFinalizeTestCase(UpdateAPITestCase):
    url_name = 'api:school_assignments_finalize'

    def setUp(self):
        self.user = TestUsers.new_user(username='regular', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.country = TestCountries.new_country()
        self.committee1 = TestCommittees.new_committee()
        self.committee2 = TestCommittees.new_committee()
        self.assignment1 = Assignment.objects.create(
            committee=self.committee1,
            country=self.country,
            school=self.school,
        )
        self.assignment2 = Assignment.objects.create(
            committee=self.committee2,
            country=self.country,
            school=self.school,
        )

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response(self.school.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It finalizes the assignments for the school's advisor.'''
        self.client.login(username='regular', password='user')
        response = self.get_response(self.school.id)
        print(response)
        print(self.school.assignments_finalized)
        self.assertFinalized(response)

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = TestUsers.new_user(username='another', password='user')
        TestSchools.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response(self.school.id)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It finalizes the assignments for a superuser.'''
        TestUsers.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response(self.school.id)
        self.assertFinalized(response)

    def assertFinalized(self, response):
        '''Assert that the school now has a finalized assignments'''
        school = School.objects.get(id=self.school.id)
        self.assertEqual(True, school.assignments_finalized)
