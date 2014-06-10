# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.accounts.models import User
from huxley.api.tests import (CreateAPITestCase, DestroyAPITestCase,
                              ListAPITestCase, PartialUpdateAPITestCase,
                              RetrieveAPITestCase)
from huxley.core.models import School
from huxley.utils.test import TestSchools, TestUsers


class SchoolDetailGetTestCase(RetrieveAPITestCase):
    url_name = 'api:school_detail'

    def test_anonymous_user(self):
        '''It should reject request from an anonymous user.'''
        school = TestSchools.new_school()
        response = self.get_response(school.id)

        self.assertNotAuthenticated(response)

    def test_self(self):
        '''It should allow the get request from the user.'''
        school = TestSchools.new_school()

        self.client.login(username='testuser', password='test')
        response = self.get_response(school.id)

        self.assertEqual(response.data, {
            'id': school.id,
            'registered': school.registered.isoformat(),
            'name': school.name,
            'address': school.address,
            'city': school.city,
            'state': school.state,
            'zip_code': school.zip_code,
            'country': school.country,
            'primary_name': school.primary_name,
            'primary_email': school.primary_email,
            'primary_phone': school.primary_phone,
            'secondary_name': school.secondary_name,
            'secondary_email': school.secondary_email,
            'secondary_phone': school.secondary_phone,
            'program_type': school.program_type,
            'times_attended': school.times_attended,
            'delegation_size': school.delegation_size,
            'international': school.international,
            'waitlist': school.waitlist})

    def test_other_user(self):
        '''it should not allow a get request from another user.'''
        school = TestSchools.new_school()
        TestUsers.new_user(username='user2', password='user2')

        self.client.login(username='user2', password='user2')
        response = self.get_response(school.id)

        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''it should allow a get request from a superuser.'''
        school = TestSchools.new_school()
        TestUsers.new_superuser(username='user1', password='user1')

        self.client.login(username='user1', password='user1')
        response = self.get_response(school.id)

        self.assertEqual(response.data, {
            'id': school.id,
            'registered': school.registered.isoformat(),
            'name': school.name,
            'address': school.address,
            'city': school.city,
            'state': school.state,
            'zip_code': school.zip_code,
            'country': school.country,
            'primary_name': school.primary_name,
            'primary_email': school.primary_email,
            'primary_phone': school.primary_phone,
            'secondary_name': school.secondary_name,
            'secondary_email': school.secondary_email,
            'secondary_phone': school.secondary_phone,
            'program_type': school.program_type,
            'times_attended': school.times_attended,
            'delegation_size': school.delegation_size,
            'international': school.international,
            'waitlist': school.waitlist})


class SchoolDetailPatchTestCase(PartialUpdateAPITestCase):
    url_name = 'api:school_detail'
    params = {'name': 'school_name', 'city': 'school_city'}

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
        self.client.login(username='testuser', password='test')
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
        '''This this allow  a superuser to change school data.'''
        TestUsers.new_superuser(username='user2', password='user2')
        self.client.login(username='user2', password='user2')
        response = self.get_response(self.school.id, params=self.params)
        self.school = School.objects.get(id=self.school.id)

        self.assertEqual(response.data['name'], self.school.name)
        self.assertEqual(response.data['city'], self.school.city)


class SchoolDetailDeleteTestCase(DestroyAPITestCase):
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
        self.client.login(username='testuser', password='test')
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


class SchoolListGetTestCase(ListAPITestCase):
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


class SchoolListPostTestCase(CreateAPITestCase):
    url_name = 'api:school_list'
    params = {'name': 'Berkeley Prep',
            'address': '1 BMUN way',
            'city': 'Oakland',
            'state': 'California',
            'zip_code': 94720,
            'country': 'USA',
            'primary_name': 'Kunal Mehta',
            'primary_email': 'KunalMehta@huxley.org',
            'primary_phone': '9999999999',
            'program_type': User.TYPE_ADVISOR}

    def test_empty_fields(self):
        '''This should not allow for required fields to be empty.'''
        response = self.get_response(params=self.get_params(name='',
                                                            address='',
                                                            city='',
                                                            state='',
                                                            zip_code='',
                                                            country='',
                                                            primary_name='',
                                                            primary_email='',
                                                            primary_phone='',
                                                            program_type=''))
        self.assertEqual(response.data,
            {"city": ["This field is required."],
            "name": ["This field is required."],
            "primary_phone": ["This field is required."],
            "program_type": ["This field is required."],
            "country": ["This field is required."],
            "state": ["This field is required."],
            "primary_name": ["This field is required."],
            "primary_email": ["This field is required."],
            "address": ["This field is required."],
            "zip_code": ["This field is required."]})

    def test_valid(self):
        params = self.get_params()
        response = self.get_response(params)

        school_query = School.objects.filter(id=response.data['id'])
        self.assertTrue(school_query.exists())

        school = School.objects.get(id=response.data['id'])
        self.assertEqual(response.data, {
            'id': school.id,
            'registered': school.registered.isoformat(),
            'name': school.name,
            'address': school.address,
            'city': school.city,
            'state': school.state,
            'zip_code': school.zip_code,
            'country': school.country,
            'primary_name': school.primary_name,
            'primary_email': school.primary_email,
            'primary_phone': school.primary_phone,
            'secondary_name': school.secondary_name,
            'secondary_email': school.secondary_email,
            'secondary_phone': school.secondary_phone,
            'program_type': school.program_type,
            'times_attended': school.times_attended,
            'delegation_size': school.delegation_size,
            'international': school.international,
            'waitlist': school.waitlist})
