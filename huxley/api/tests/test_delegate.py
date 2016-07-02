# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api.tests import (CreateAPITestCase, DestroyAPITestCase,
                              PartialUpdateAPITestCase, UpdateAPITestCase)
from huxley.api.tests import auto
from huxley.api.views.delegate import DelegateDetail
from huxley.utils.test import (TestUsers, TestSchools, TestAssignments,
                               TestDelegates)


class DelegateDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:delegate_detail'
    view = DelegateDetail

    @classmethod
    def get_test_object(cls):
        user = TestUsers.new_user(username='user', password='user')
        school = TestSchools.new_school(user=user)
        assignment = TestAssignments.new_assignment(school=school)
        return TestDelegates.new_delegate(assignment=assignment)

    @classmethod
    def get_users(cls, test_object):
        TestUsers.new_superuser(username='superuser', password='superuser')
        return (
            (None, None, cls.NOT_AUTHENTICATED),
            ('user', 'user', None),
            ('superuser', 'superuser', None),
        )


class DelegateDetailPutTestCase(UpdateAPITestCase):
    url_name = 'api:delegate_detail'
    params = {
        'name':'Trevor Dowds',
        'email':'tdowds@hotmail.org',
        'summary':'He did awful!'}

    def setUp(self):
        self.user = TestUsers.new_user(username='user', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.assignment = TestAssignments.new_assignment(school=self.school)
        self.delegate = TestDelegates.new_delegate(assignment=self.assignment)
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
            "assignment" : self.delegate.assignment.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary'])}
        )

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = TestUsers.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id" : self.delegate.id,
            "assignment" : self.delegate.assignment.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary'])}
        )


class DelegateDetailPatchTestCase(PartialUpdateAPITestCase):
    url_name = 'api:delegate_detail'
    params = {
        'name':'Trevor Dowds',
        'email':'tdowds@hotmail.org',
        'summary':'He did awful!'}

    def setUp(self):
        self.user = TestUsers.new_user(username='user', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.assignment = TestAssignments.new_assignment(school=self.school)
        self.delegate = TestDelegates.new_delegate(assignment=self.assignment)

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
            "assignment" : self.delegate.assignment.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary'])}
        )

    def test_superuser(self):
        '''It should return correct data allowing a partial update.'''
        superuser = TestUsers.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id" : self.delegate.id,
            "assignment" : self.delegate.assignment.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary'])}
        )


class DelegateDetailDeleteTestCase(DestroyAPITestCase):
    url_name = 'api:delegate_detail'

    def setUp(self):
        self.user = TestUsers.new_user(username='user', password='user')
        self.school = TestSchools.new_school(user=self.user)
        self.assignment = TestAssignments.new_assignment(school=self.school)
        self.delegate = TestDelegates.new_delegate(assignment=self.assignment)

    def test_anonymous_user(self):
        '''Unauthenticated users should not be able to delete assignments.'''
        response = self.get_response(self.assignment.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Authenticated users shouldn't have permission to delete assignments.'''
        self.client.login(username='user', password='user')

        response = self.get_response(self.assignment.id)
        self.assert204(response)

    def test_superuser(self):
        '''Assignments should not be able to be deleted through API'''
        TestUsers.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')

        response = self.get_response(self.assignment.id)
        self.assert204(response)

class DelegateListCreateTestCase(CreateAPITestCase):
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

    def test_anonymous_user(self):
        '''Should accept post request from any user.'''
        response = self.get_response(params=self.params)
        response.data.pop('created_at')
        response.data.pop('id')
        self.assertEqual(response.data, {
            "assignment" : self.assignment.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary'])}
        )

    def test_advisor(self):
        '''Should allow advisors to create new delegates.'''
        self.client.login(username='user', password='user')
        response = self.get_response(params=self.params)
        response.data.pop('created_at')
        response.data.pop('id')
        self.assertEqual(response.data, {
            "assignment" : self.assignment.id,
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary'])}
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
            "name" : unicode(self.params['name']),
            "email" : unicode(self.params['email']),
            "summary" : unicode(self.params['summary'])}
        )
