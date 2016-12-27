# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api.tests import UpdateAPITestCase
from huxley.core.models import Assignment, School
from huxley.utils.test import (TestCommittees, TestCountries, TestSchools,
                               TestUsers)


class SchoolAssignmentsFinalizeTestCase(UpdateAPITestCase):
    url_name = 'api:school_detail'
    params = {'assignments_finalized': True}

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
        school = School.objects.get(name=self.school.name)
        self.assertEqual(True, school.assignments_finalized)


class SchoolAssignmentsDeleteTestCase(UpdateAPITestCase):
    url_name = 'api:assignment_detail'
    params = {'rejected': True}

    def setUp(self):
        self.user = TestUsers.new_user(username='regular', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.country = TestCountries.new_country()
        self.committee = TestCommittees.new_committee()
        self.assignment = Assignment.objects.create(
            committee=self.committee,
            country=self.country,
            school=self.school,
        )

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response(self.assignment.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It finalizes the assignments for the school's advisor.'''
        self.client.login(username='regular', password='user')
        response = self.get_response(self.assignment.id)
        self.assertDeleted(response)

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = TestUsers.new_user(username='another', password='user')
        TestSchools.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response(self.assignment.id)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It finalizes the assignments for a superuser.'''
        TestUsers.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response(self.assignment.id)
        self.assertDeleted(response)

    def assertDeleted(self, response):
        '''Assert that the school now has a finalized assignments'''
        assignment = Assignment.objects.get(id=self.assignment.id)
        self.assertEqual(response.data,
            {
                'id': assignment.id,
                'country': self.country.id,
                'committee': self.committee.id,
                'school': self.school.id,
                'rejected': assignment.rejected,
            }
        )
