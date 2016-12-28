# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api import tests
from huxley.api.tests import auto
from huxley.core.models import School
from huxley.utils.test import models


class SchoolDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:school_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_school()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        self.as_user(self.object.advisor).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()


class SchoolDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:school_detail'
    params = {'name': 'name', 'city': 'city'}

    def setUp(self):
        self.school = models.new_school()
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
        models.new_user(username='user2', password='user2')
        self.client.login(username='user2', password='user2')
        response = self.get_response(self.school.id, params=self.params)
        updated_school = School.objects.get(id=self.school.id)

        self.assertPermissionDenied(response)
        self.assertEqual(updated_school.name, self.school.name)
        self.assertEqual(updated_school.city, self.school.city)

    def test_superuser(self):
        '''This should allow  a superuser to change school data.'''
        models.new_superuser(username='user2', password='user2')
        self.client.login(username='user2', password='user2')
        response = self.get_response(self.school.id, params=self.params)
        self.school = School.objects.get(id=self.school.id)

        self.assertEqual(response.data['name'], self.school.name)
        self.assertEqual(response.data['city'], self.school.city)


class SchoolDetailDeleteTestCase(auto.DestroyAPIAutoTestCase):
    url_name = 'api:school_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_school()

    def test_anonymous_user(self):
        '''Anonymous users cannot delete a school.'''
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        '''Advisors can delete their school.'''
        self.as_user(self.object.advisor).do_test()

    def test_other_user(self):
        '''A user cannot delete another user's school.'''
        self.as_default_user().do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_superuser(self):
        '''A superuser can delete a school.'''
        self.as_superuser().do_test()


class SchoolListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:school_list'

    def setUp(self):
        self.school = models.new_school()
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
        models.new_superuser(username='user', password='user')

        self.client.login(username='user', password='user')
        response = self.get_response()

        self.assertMethodNotAllowed(response, 'GET')
