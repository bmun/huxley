# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api import tests
from huxley.api.tests import auto
from huxley.core.models import School
from huxley.utils.test import TestSchools, TestUsers

from huxley.api.views.school import SchoolDetail


class SchoolDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:school_detail'
    view = SchoolDetail

    @classmethod
    def get_test_object(cls):
        return TestSchools.new_school()

    @classmethod
    def get_users(cls, test_object):
        TestUsers.new_superuser(username='user1', password='user1')
        return (
            (None, None, cls.NOT_AUTHENTICATED),
            (test_object.advisor.username, 'test', None),
            ('user1', 'user1', None),
        )


class SchoolDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:school_detail'
    params = {'name': 'name', 'city': 'city'}

    def setUp(self):
        self.school = TestSchools.new_school()
        self.user = self.school.advisor

    def test_anonymous_user(self):
        '''Should not be able to update with an anonymous user.'''
        response = self.get_response(self.school.id)
        updated_school = School.objects.get(id=self.school.id)

        self.assertNotAuthenticated(response)
        self.assertEqual(updated_school.name, self.school.name)
        self.assertEqual(updated_school.city, self.school.city)

    def test_self(self):
        '''You should be able to update with an anonymous user.'''
        self.client.login(username=self.user.username, password='test')
        response = self.get_response(self.school.id, params=self.params)
        self.school = School.objects.get(id=self.school.id)

        self.assertEqual(response.data['name'], self.school.name)
        self.assertEqual(response.data['city'], self.school.city)

    def test_other_user(self):
        '''Should not allow another user to change a school's data'''
        TestUsers.new_user(username='user2', password='user2')
        self.client.login(username='user2', password='user2')
        response = self.get_response(self.school.id, params=self.params)
        updated_school = School.objects.get(id=self.school.id)

        self.assertPermissionDenied(response)
        self.assertEqual(updated_school.name, self.school.name)
        self.assertEqual(updated_school.city, self.school.city)

    def test_superuser(self):
        '''This should allow  a superuser to change school data.'''
        TestUsers.new_superuser(username='user2', password='user2')
        self.client.login(username='user2', password='user2')
        response = self.get_response(self.school.id, params=self.params)
        self.school = School.objects.get(id=self.school.id)

        self.assertEqual(response.data['name'], self.school.name)
        self.assertEqual(response.data['city'], self.school.city)


class SchoolDetailDeleteTestCase(tests.DestroyAPITestCase):
    url_name = 'api:school_detail'

    def setUp(self):
        self.school = TestSchools.new_school()
        self.user = self.school.advisor

    def test_anonymous_user(self):
        '''Should not be able to delete anonymously.'''
        response = self.get_response(self.school.id)

        self.assertNotAuthenticated(response)
        self.assertTrue(School.objects.filter(id=self.school.id).exists())

    def test_self(self):
        '''One user should be able to delete their own account.'''
        self.client.login(username=self.user.username, password='test')
        response = self.get_response(self.school.id)

        self.assertEqual(response.data, None)
        self.assertFalse(School.objects.filter(id=self.school.id).exists())

    def test_other_user(self):
        '''One user should not be able to delete another user.'''
        TestUsers.new_user(username='user2', password='user2')
        self.client.login(username='user2', password='user2')
        response = self.get_response(self.school.id)

        self.assertPermissionDenied(response)
        self.assertTrue(School.objects.filter(id=self.school.id).exists())

    def test_superuser(self):
        '''A superuser should not be able to delete an account.'''
        TestUsers.new_user(username='user2', password='user2')
        self.client.login(username='user2', password='user2')
        response = self.get_response(self.school.id)

        self.assertPermissionDenied(response)
        self.assertTrue(School.objects.filter(id=self.school.id).exists())


class SchoolListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:school_list'

    def setUp(self):
        self.school = TestSchools.new_school()
        self.user = self.school.advisor

    def test_anonymous_user(self):
        '''It should reject an anonymous user.'''
        response = self.get_response()

        self.assertMethodNotAllowed(response, 'GET')

    def test_self(self):
        '''It should reject a request from an unauthorized user.'''
        self.client.login(username='testuser', password='test')
        response = self.get_response()

        self.assertMethodNotAllowed(response, 'GET')

    def test_superuser(self):
        '''It should reject a request from a superuser.'''
        TestUsers.new_superuser(username='user', password='user')

        self.client.login(username='user', password='user')
        response = self.get_response()

        self.assertMethodNotAllowed(response, 'GET')
