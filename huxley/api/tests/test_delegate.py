# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.exceptions import ValidationError

from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models


class DelegateDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:delegate_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_delegate()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        self.as_user(self.object.school.advisor).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()


class DelegateDetailPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:delegate_detail'
    params = {
        'name':'Trevor Dowds',
        'email':'tdowds@hotmail.org',
        'summary':'He did awful!'}

    def setUp(self):
        self.user = models.new_user(username='user', password='user')
        self.school = models.new_school(user=self.user)
        self.assignment = models.new_assignment(school=self.school)
        self.delegate = models.new_delegate(assignment=self.assignment, school=self.school)
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
        superuser = models.new_superuser(username='s_user', password='s_user')
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
        self.user = models.new_user(username='user', password='user')
        self.school = models.new_school(user=self.user)
        self.assignment = models.new_assignment(school=self.school)
        self.delegate = models.new_delegate(assignment=self.assignment, school=self.school)

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
        superuser = models.new_superuser(username='s_user', password='s_user')
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
        return models.new_delegate()

    def test_anonymous_user(self):
        '''Anonymous users cannot delete delegates.'''
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        '''Advisors can delete their delegates.'''
        self.as_user(self.object.school.advisor).do_test()

    def test_other_user(self):
        '''A user cannot delete another user's delegates.'''
        models.new_school(user=self.default_user)
        self.as_default_user().do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_superuser(self):
        '''A superuser can delete delegates.'''
        self.as_superuser().do_test()


class DelegateListCreateTestCase(tests.CreateAPITestCase):
    url_name = 'api:delegate_list'
    params = {
        'name':'Trevor Dowds',
        'email':'tdowds@hotmail.org',
        'summary':'He did awful!'}

    def setUp(self):
        self.user = models.new_user(username='user', password='user')
        self.school = models.new_school(user=self.user)
        self.assignment = models.new_assignment(school=self.school)
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
        superuser = models.new_superuser(username='s_user', password='s_user')
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


class DelegateListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:delegate_list'

    def setUp(self):
        self.user = models.new_user(username='regular', password='user')
        self.school = models.new_school(user=self.user)
        self.country = models.new_country()
        self.committee1 = models.new_committee()
        self.committee2 = models.new_committee()
        self.assignment1 = models.new_assignment(
            committee=self.committee1,
            country=self.country,
            school=self.school,
        )
        self.assignment2 = models.new_assignment(
            committee=self.committee2,
            country=self.country,
            school=self.school,
        )
        self.delegate1 = models.new_delegate(
            assignment=self.assignment1,
        )
        self.delegate2 = models.new_delegate(
            assignment=self.assignment2,
            name='Trevor Dowds',
            email='t@dowds.com',
            summary='Good!'
        )

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response(self.school.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It returns the delegates for the school's advisor.'''
        self.client.login(username='regular', password='user')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(params={'school_id': self.school.id})
        self.assert_delegate_equal(response)

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = models.new_user(username='another', password='user')
        models.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response(self.school.id)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It returns the delegates for a superuser.'''
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response(self.school.id)
        self.assert_delegate_equal(response)

    def assert_delegate_equal(self, response):
        '''Assert that the response contains the delegates in order.'''
        response.data[0].pop('created_at')
        response.data[1].pop('created_at')
        self.assertEqual(dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.assignment1.id,
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
            },
        )
        self.assertEqual(dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.assignment2.id,
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
            },
        )


class DelegateListPartialUpdateTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:delegate_list'
    is_resource = False

    def setUp(self):
        self.user = models.new_user(username='regular', password='user')
        self.school = models.new_school(user=self.user)

        self.country = models.new_country()
        self.committee1 = models.new_committee()
        self.committee2 = models.new_committee()
        self.committee3 = models.new_committee()
        self.committee4 = models.new_committee()

        self.assignment1 = models.new_assignment(
            school=self.school,
            country=self.country,
            commitee=self.committee3
        )

        self.assignment2 = models.new_assignment(
            school=self.school,
            country=self.country,
            committee=self.committee2
        )

        self.new_assignment = models.new_assignment(
            school=self.school,
            country=self.country,
            committee=self.committee3
        )

        self.faulty_assignment = models.new_assignment(
            country=self.country,
            committee=self.committee4
        )

        self.delegate1 = models.new_delegate(
            name="Nathaniel Parke",
            school=self.school,
            assignment=self.assignment1
        )

        self.delegate2 = models.new_delegate(
            name='Trevor Dowds',
            school=self.school,
            assignment=self.assignment2
        )

        self.params = [
            {'id': self.delegate1.id, 'assignment': self.new_assignment.id},
            {'id': self.delegate2.id, 'assignment': None}
        ]

    def test_anonymous_user(self):
        '''Should accept a partial update from any user.'''
        response = self.get_response()
        self.assertEqual(dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.params[0]['assignment'],
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'created_at': self.delegate1.created_at.isoformat()
            },
        )
        self.assertEqual(dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.params[1]['assignment'],
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
                'created_at': self.delegate2.created_at.isoformat()
            },
        )

    def test_advisor(self):
        '''It updates the delegates for the school's advisor.'''
        self.client.login(username='regular', password='user')

        response = self.get_response()
        self.assertEqual(dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.params[0]['assignment'],
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'created_at': self.delegate1.created_at.isoformat()
            },
        )
        self.assertEqual(dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.params[1]['assignment'],
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
                'created_at': self.delegate2.created_at.isoformat()
            },
        )

    def test_advisor_fail(self):
        '''
        It doesn't update the delegates for the school's advisor if fields
        are invalid.
        '''
        self.client.login(username='regular', password='user')
        self.params = [
            {'id': self.delegate1.id, 'assignment': self.faulty_assignment.id},
            {'id': self.delegate2.id, 'assignment': self.new_assignment.id}
        ]

        self.assertRaises(ValidationError, self.get_response, self.school.id)

    def test_other_user(self):
        '''Should accept a partial update from another user.'''
        user2 = models.new_user(username='another', password='user')
        models.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response()
        self.assertEqual(dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.params[0]['assignment'],
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'created_at': self.delegate1.created_at.isoformat()
            },
        )
        self.assertEqual(dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.params[1]['assignment'],
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
                'created_at': self.delegate2.created_at.isoformat()
            },
        )

    def test_superuser(self):
        '''It updates the delegates for a superuser.'''
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response(self.school.id)
        self.assertEqual(dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.params[0]['assignment'],
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'created_at': self.delegate1.created_at.isoformat()
            },
        )
        self.assertEqual(dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.params[1]['assignment'],
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
                'created_at': self.delegate2.created_at.isoformat()
            },
        )

    def test_superuser_fail(self):
        '''
        It doesn't update the delegates for the superuser if fields are invalid.
        '''
        self.client.login(username='regular', password='user')
        self.params = [
            {'id': self.delegate1.id, 'assignment': self.faulty_assignment.id},
            {'id': self.delegate2.id, 'assignment': self.new_assignment.id}
        ]

        self.assertRaises(ValidationError, self.get_response, self.school.id)
