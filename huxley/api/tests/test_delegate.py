# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import (TestUsers, TestSchools, TestAssignments,
                               TestDelegates)


class DelegateDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:delegate_detail'

    @classmethod
    def get_test_object(cls):
        user = TestUsers.new_user(username='user', password='user')
        school = TestSchools.new_school(user=user)
        assignment = TestAssignments.new_assignment(school=school)
        return TestDelegates.new_delegate(assignment=assignment)

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        self.do_test(username='user', password='user')

    def test_superuser(self):
        TestUsers.new_superuser(username='superuser', password='superuser')
        self.do_test(username='superuser', password='superuser')


class DelegateDetailPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:delegate_detail'
    params = {
        'name':'Trevor Dowds',
        'email':'tdowds@hotmail.org',
        'summary':'He did awful!'}

    def setUp(self):
        self.user = TestUsers.new_user(username='user', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.assignment = TestAssignments.new_assignment(school=self.school)
        self.delegate = TestDelegates.new_delegate(assignment=self.assignment, school=self.school)
        self.params['assignment'] = self.assignment.id

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update assignments.'''
        response = self.get_response(self.delegate.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It should return correct data.'''
        self.client.login(username='user', password='user')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id" : self.delegate.id,
            "assignment" : self.assignment.id,
            "school" : self.school.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary']),}
        )

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = TestUsers.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id" : self.delegate.id,
            "assignment" : self.assignment.id,
            "school" : self.school.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary']),}
        )


class DelegateDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:delegate_detail'
    params = {
        'name':'Trevor Dowds',
        'email':'tdowds@hotmail.org',
        'summary':'He did awful!'}

    def setUp(self):
        self.user = TestUsers.new_user(username='user', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.assignment = TestAssignments.new_assignment(school=self.school)
        self.delegate = TestDelegates.new_delegate(assignment=self.assignment, school=self.school)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update assignments.'''
        response = self.get_response(self.delegate.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It should return correct data allowing a partial update.'''
        self.client.login(username='user', password='user')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id" : self.delegate.id,
            "assignment" : self.assignment.id,
            "school" : self.school.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary']),}
        )

    def test_superuser(self):
        '''It should return correct data allowing a partial update.'''
        superuser = TestUsers.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id" : self.delegate.id,
            "assignment" : self.assignment.id,
            "school" : self.school.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary']),}
        )


class DelegateDetailDeleteTestCase(auto.DestroyAPIAutoTestCase):
    url_name = 'api:delegate_detail'

    @classmethod
    def get_test_object(cls):
        return TestDelegates.new_delegate()

    def test_anonymous_user(self):
        '''Anonymous users cannot delete delegates.'''
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        '''Advisors can delete their delegates.'''
        self.do_test(
            username=self.object.school.advisor.username,
            password='test')

    def test_other_user(self):
        '''A user cannot delete another user's delegates.'''
        joe = TestUsers.new_user(username='joe', password='schmoe')
        TestSchools.new_school(user=joe)
        self.do_test(
            username='joe', password='schmoe',
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_superuser(self):
        '''A superuser can delete delegates.'''
        TestUsers.new_superuser(username='super', password='super')
        self.do_test(username='super', password='super')


class DelegateListCreateTestCase(tests.CreateAPITestCase):
    url_name = 'api:delegate_list'
    params = {
        'name':'Trevor Dowds',
        'email':'tdowds@hotmail.org',
        'summary':'He did awful!'}

    def setUp(self):
        self.user = TestUsers.new_user(username='user', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.assignment = TestAssignments.new_assignment(school=self.school)
        self.params['assignment'] = self.assignment.id
        self.params['school'] = self.school.id

    def test_anonymous_user(self):
        '''Should accept post request from any user.'''
        response = self.get_response(params=self.params)
        response.data.pop('created_at')
        response.data.pop('id')
        self.assertEqual(response.data, {
            "assignment" : self.assignment.id,
            "school" : self.school.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary']),}
        )

    def test_advisor(self):
        '''Should allow advisors to create new delegates.'''
        self.client.login(username='user', password='user')
        response = self.get_response(params=self.params)
        response.data.pop('created_at')
        response.data.pop('id')
        self.assertEqual(response.data, {
            "assignment" : self.assignment.id,
            "school" : self.school.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary']),}
        )

    def test_superuser(self):
        '''Should allow superuser to create delegate.'''
        superuser = TestUsers.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(params=self.params)
        response.data.pop('created_at')
        response.data.pop('id')
        self.assertEqual(response.data, {
            "assignment" : self.assignment.id,
            "school" : self.school.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary']),}
        )
