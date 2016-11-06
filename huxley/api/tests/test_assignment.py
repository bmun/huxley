# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import (TestUsers, TestSchools, TestAssignments,
                               TestCommittees, TestCountries)


class AssignmentDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:assignment_detail'

    @classmethod
    def get_test_object(cls):
        return TestAssignments.new_assignment()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        self.as_user(self.object.school.advisor).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()


class AssignmentDetailPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:assignment_detail'
    params = {'rejected':True}

    def setUp(self):
        self.user = TestUsers.new_user(username='user', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.assignment = TestAssignments.new_assignment(school=self.school)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update assignments.'''
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It should return correct data.'''
        self.client.login(username='user', password='user')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertEqual(response.data, {
            "id" : self.assignment.id,
            "committee" : self.assignment.committee.id,
            "country" : self.assignment.country.id,
            "school" : self.school.id,
            "rejected" : True,
        })

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = TestUsers.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.assignment.id)
        self.assertEqual(response.data, {
            "id" : self.assignment.id,
            "committee" : self.assignment.committee.id,
            "country" : self.assignment.country.id,
            "school" : self.school.id,
            "rejected" : True,
        })


class AssignmentDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:assignment_detail'
    params = {'rejected':True}

    def setUp(self):
        self.user = TestUsers.new_user(username='user', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.assignment = TestAssignments.new_assignment(school=self.school)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update assignments.'''
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It should return correct data.'''
        self.client.login(username='user', password='user')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertEqual(response.data, {
            "id" : self.assignment.id,
            "committee" : self.assignment.committee.id,
            "country" : self.assignment.country.id,
            "school" : self.school.id,
            "rejected" : True,
        })

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = TestUsers.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.assignment.id)
        self.assertEqual(response.data, {
            "id" : self.assignment.id,
            "committee" : self.assignment.committee.id,
            "country" : self.assignment.country.id,
            "school" : self.school.id,
            "rejected" : True,
        })


class AssignmentDetailDeleteTestCase(auto.DestroyAPIAutoTestCase):
    url_name = 'api:assignment_detail'

    @classmethod
    def get_test_object(cls):
        return TestAssignments.new_assignment()

    def test_anonymous_user(self):
        '''Anonymous users cannot delete assignments.'''
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        '''Advisors cannot delete their assignments.'''
        self.as_user(self.object.school.advisor).do_test(expected_error=auto.EXP_DELETE_NOT_ALLOWED)

    def test_other_user(self):
        '''A user cannot delete another user's assignments.'''
        TestSchools.new_school(user=self.default_user)
        self.as_default_user().do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_superuser(self):
        '''A superuser cannot delete assignments.'''
        self.as_superuser().do_test(expected_error=auto.EXP_DELETE_NOT_ALLOWED)


class AssignmentListCreateTestCase(tests.CreateAPITestCase):
    url_name = 'api:assignment_list'
    params = {'rejected':True}

    def setUp(self):
        self.user = TestUsers.new_user(username='user', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.committee = TestCommittees.new_committee()
        self.country = TestCountries.new_country()
        self.params['committee'] = self.committee.id
        self.params['school'] = self.school.id
        self.params['country'] = self.country.id

    def test_anonymous_user(self):
        '''Anonymous Users should not be able to create assignments.'''
        response = self.get_response(params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors should not be able to create Assignments.'''
        self.client.login(username='user', password='user')
        response = self.get_response(params=self.params)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''Superusers should be able to create assignments.'''
        TestUsers.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')

        response = self.get_response(params=self.params)
        response.data.pop('id')
        self.assertEqual(response.data, {
            "committee" : self.committee.id,
            "country" : self.country.id,
            "school" : self.school.id,
            "rejected" : True,
        })

