# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api.tests import (DestroyAPITestCase, ListAPITestCase,
                              PartialUpdateAPITestCase, RetrieveAPITestCase)
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
            'primary_gender': school.primary_gender,
            'primary_email': school.primary_email,
            'primary_phone': school.primary_phone,
            'primary_type': school.primary_type,
            'secondary_name': school.secondary_name,
            'secondary_gender': school.secondary_gender,
            'secondary_email': school.secondary_email,
            'secondary_phone': school.secondary_phone,
            'secondary_type': school.secondary_type,
            'program_type': school.program_type,
            'times_attended': school.times_attended,
            'international': school.international,
            'waitlist': school.waitlist,
            'beginner_delegates':school.beginner_delegates,
            'intermediate_delegates': school.intermediate_delegates,
            'advanced_delegates': school.advanced_delegates,
            'spanish_speaking_delegates': school.spanish_speaking_delegates,
            'prefers_bilingual': school.prefers_bilingual,
            'prefers_specialized_regional': school.prefers_specialized_regional,
            'prefers_crisis': school.prefers_crisis,
            'prefers_alternative': school.prefers_alternative,
            'prefers_press_corps': school.prefers_press_corps,
            'registration_comments': school.registration_comments,
            'fees_owed': float(school.fees_owed),
            'fees_paid': float(school.fees_paid),
        })

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
            'primary_gender': school.primary_gender,
            'primary_email': school.primary_email,
            'primary_phone': school.primary_phone,
            'primary_type': school.primary_type,
            'secondary_name': school.secondary_name,
            'secondary_gender': school.secondary_gender,
            'secondary_email': school.secondary_email,
            'secondary_phone': school.secondary_phone,
            'secondary_type': school.secondary_type,
            'program_type': school.program_type,
            'times_attended': school.times_attended,
            'international': school.international,
            'waitlist': school.waitlist,
            'beginner_delegates': school.beginner_delegates,
            'intermediate_delegates': school.intermediate_delegates,
            'advanced_delegates': school.advanced_delegates,
            'spanish_speaking_delegates': school.spanish_speaking_delegates,
            'prefers_bilingual': school.prefers_bilingual,
            'prefers_specialized_regional': school.prefers_specialized_regional,
            'prefers_crisis': school.prefers_crisis,
            'prefers_alternative': school.prefers_alternative,
            'prefers_press_corps': school.prefers_press_corps,
            'registration_comments': school.registration_comments,
            'fees_owed': float(school.fees_owed),
            'fees_paid': float(school.fees_paid),
        })


class SchoolDetailPatchTestCase(PartialUpdateAPITestCase):
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
        '''This should allow  a superuser to change school data.'''
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
