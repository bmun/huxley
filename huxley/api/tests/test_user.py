# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.accounts.models import User
from huxley.core.models import Conference
from huxley.api.tests import (CreateAPITestCase, DestroyAPITestCase,
                              ListAPITestCase, PartialUpdateAPITestCase,
                              RetrieveAPITestCase)
from huxley.utils.test import TestSchools, TestUsers


class UserDetailGetTestCase(RetrieveAPITestCase):
    url_name = 'api:user_detail'

    def test_anonymous_user(self):
        '''It should reject request from an anonymous user.'''
        user = TestUsers.new_user()
        response = self.get_response(user.id)

        self.assertNotAuthenticated(response)

    def test_other_user(self):
        '''It should reject request from another user.'''
        user1 = TestUsers.new_user(username='user1')
        user2 = TestUsers.new_user(username='user2', password='user2')

        self.client.login(username='user2', password='user2')
        response = self.get_response(user1.id)

        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It should return the correct fields for a superuser.'''
        user1 = TestUsers.new_user(username='user1')
        user2 = TestUsers.new_superuser(username='user2', password='user2')

        self.client.login(username='user2', password='user2')
        response = self.get_response(user1.id)

        self.assertEqual(response.data, {
            'id': user1.id,
            'username': user1.username,
            'first_name': user1.first_name,
            'last_name': user1.last_name,
            'user_type': user1.user_type,
            'school': user1.school_id,
            'committee': user1.committee_id})

    def test_self(self):
        '''It should return the correct fields for a single user.'''
        school = TestSchools.new_school()
        user = school.advisor
        self.client.login(username=user.username, password='test')
        response = self.get_response(user.id)

        self.assertEqual(response.data, {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
            'school': {
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
                'chinese_speaking_delegates': school.chinese_speaking_delegates,
                'countrypreferences': school.country_preference_ids,
                'committeepreferences': list(school.committeepreferences.all()),
                'registration_comments': school.registration_comments,
                'fees_owed': float(school.fees_owed),
                'fees_paid': float(school.fees_paid),
                'assignments_finalized': school.assignments_finalized,
                'delegate_names_finalized': school.delegate_names_finalized,
            },
            'committee': user.committee_id})

    def test_chair(self):
        '''It should have the correct fields for chairs.'''
        user = TestUsers.new_user(user_type=User.TYPE_CHAIR,
                                  committee_id=4)
        self.client.login(username='testuser', password='test')
        response = self.get_response(user.id)

        self.assertEqual(response.data, {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
            'school': user.school_id,
            'committee': user.committee_id})


class UserDetailDeleteTestCase(DestroyAPITestCase):
    url_name = 'api:user_detail'

    def setUp(self):
        self.user = TestUsers.new_user(username='user1', password='user1')

    def test_anonymous_user(self):
        '''It should reject the request from an anonymous user.'''
        response = self.get_response(self.user.id)

        self.assertNotAuthenticated(response)
        self.assertTrue(User.objects.filter(id=self.user.id).exists())

    def test_other_user(self):
        '''It should reject the request from another user.'''
        TestUsers.new_user(username='user2', password='user2')
        self.client.login(username='user2', password='user2')

        response = self.get_response(self.user.id)
        self.assertPermissionDenied(response)
        self.assertTrue(User.objects.filter(id=self.user.id).exists())

    def test_self(self):
        '''It should allow a user to delete themself.'''
        self.client.login(username='user1', password='user1')

        response = self.get_response(self.user.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_superuser(self):
        '''It should allow a superuser to delete a user.'''
        TestUsers.new_superuser(username='user2', password='user2')
        self.client.login(username='user2', password='user2')

        response = self.get_response(self.user.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class UserDetailPatchTestCase(PartialUpdateAPITestCase):
    url_name = 'api:user_detail'
    params = {'first_name': 'first',
              'last_name': 'last'}

    def setUp(self):
        self.user = TestUsers.new_user(username='user1', password='user1')

    def test_anonymous_user(self):
        '''An anonymous user should not be able to change information.'''
        response = self.get_response(self.user.id, params=self.params)
        self.assertNotAuthenticated(response)

        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

    def test_other_user(self):
        '''Another user should not be able to change information about any other user.'''
        TestUsers.new_user(username='user2', password='user2')
        self.client.login(username='user2', password='user2')

        response = self.get_response(self.user.id, params=self.params)
        self.assertPermissionDenied(response)

        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

    def test_self(self):
        '''A User should be allowed to change information about himself.'''
        self.client.login(username='user1', password='user1')

        response = self.get_response(self.user.id, params=self.params)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)

    def test_superuser(self):
        '''A superuser should be allowed to change information about a user.'''
        TestUsers.new_superuser(username='user2', password='user2')
        self.client.login(username='user2', password='user2')

        response = self.get_response(self.user.id, params=self.params)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)


class UserListGetTestCase(ListAPITestCase):
    url_name = 'api:user_list'

    def test_anonymous_user(self):
        '''It should reject the request from an anonymous user.'''
        TestUsers.new_user(username='user1')
        TestUsers.new_user(username='user2')

        response = self.get_response()
        self.assertNotAuthenticated(response)

    def test_user(self):
        '''It should reject the request from a regular user.'''
        TestUsers.new_user(username='user1', password='user1')
        TestUsers.new_user(username='user2')
        self.client.login(username='user1', password='user1')

        response = self.get_response()
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It should allow a superuser to list all users.'''
        user1 = TestUsers.new_superuser(username='user1', password='user1')
        user2 = TestUsers.new_user(username='user2')
        self.client.login(username='user1', password='user1')

        response = self.get_response()
        self.assertEqual(response.data, [
            {'id': user1.id,
             'username': user1.username,
             'first_name': user1.first_name,
             'last_name': user1.last_name,
             'user_type': user1.user_type,
             'school': user1.school_id,
             'committee': user1.committee_id},
            {'id': user2.id,
             'username': user2.username,
             'first_name': user2.first_name,
             'last_name': user2.last_name,
             'user_type': user2.user_type,
             'school': user2.school_id,
             'committee': user2.committee_id}])


class UserListPostTestCase(CreateAPITestCase):
    url_name = 'api:user_list'
    params = {'username': 'Kunal',
              'password': 'password',
              'first_name': 'Kunal',
              'last_name': 'Mehta'}

    def test_valid(self):
        params = self.get_params()
        response = self.get_response(params)

        user_query = User.objects.filter(id=response.data['id'])
        self.assertTrue(user_query.exists())

        user = User.objects.get(id=response.data['id'])
        self.assertEqual(response.data, {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': User.TYPE_ADVISOR,
            'school': user.school_id,
            'email': user.email})

    def test_empty_username(self):
        response = self.get_response(params=self.get_params(username=''))
        self.assertEqual(response.data, {
            'username': [u'This field may not be blank.']})

    def test_taken_username(self):
        TestUsers.new_user(username='_Kunal', password='pass')
        response = self.get_response(params=self.get_params(username='_Kunal'))
        self.assertEqual(response.data, {
            'username': [u'A user with that username already exists.']})

    def test_invalid_username(self):
        response = self.get_response(params=self.get_params(username='>Kunal'))
        self.assertEqual(response.data, {
            'username': [
                u'Enter a valid username. This value may contain only letters, '
                u'numbers and @/./+/-/_ characters.']})

    def test_empty_password(self):
        response = self.get_response(params=self.get_params(password=''))
        self.assertEqual(response.data, {
            'password': [u'This field may not be blank.']})

    def test_invalid_password(self):
        response = self.get_response(params=self.get_params(password='>pass'))
        self.assertEqual(response.data, {
            'password': ['Password contains invalid characters.']})

    def test_empty_first_name(self):
        response = self.get_response(params=self.get_params(first_name=''))
        self.assertEqual(response.data, {
            'first_name': ['This field is required.']})

    def test_empty_last_name(self):
        response = self.get_response(params=self.get_params(last_name=''))
        self.assertEqual(response.data, {
            'last_name': ['This field is required.']})

    def test_username_length(self):
        response = self.get_response(params=self.get_params(username='user'))
        self.assertEqual(response.data, {
            'username': ['Username must be at least 5 characters.']})

    def test_password_length(self):
        response = self.get_response(params=self.get_params(password='pass'))
        self.assertEqual(response.data, {
            'password': ['Password must be at least 6 characters.']})

    def test_invalid(self):
        conf = Conference.get_current()
        conf.open_reg = False
        conf.save()

        params = self.get_params()
        response = self.get_response(params)
        self.assertEqual(response.data, {
            'detail': 'Conference registration is closed.'})

        conf.open_reg = True
        conf.save()


class CurrentUserTestCase(TestCase):
    fixtures = ['conference']

    def setUp(self):
        self.client = Client()
        self.url = reverse('api:current_user')
        self.maxDiff = None

    def get_data(self, url):
        return json.loads(self.client.get(url).content)

    def test_login(self):
        user = TestUsers.new_user(username='lol', password='lol')
        user2 = TestUsers.new_user(username='bunny', password='bunny')

        credentials = {'username': 'lol', 'password': 'lol'}
        response = self.client.post(self.url,
                                    data=json.dumps(credentials),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)


        credentials = {'username': 'bunny', 'password': 'bunny'}
        response = self.client.post(self.url,
                                    data=json.dumps(credentials),
                                    content_type='application/json')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

        data = json.loads(response.content)
        self.assertEqual(data['detail'],
                         'Another user is currently logged in.')

    def test_logout(self):
        user = TestUsers.new_user(username='lol', password='lol')

        self.client.login(username='lol', password='lol')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertTrue('_auth_user_id' not in self.client.session)

    def test_get(self):
        data = self.get_data(self.url)

        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'], u'Not found.')

        school = TestSchools.new_school()
        user = school.advisor
        self.client.login(username=user.username, password='test')

        data = self.get_data(self.url)
        self.assertEqual(len(data.keys()), 7)
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['username'], user.username)
        self.assertEqual(data['first_name'], user.first_name)
        self.assertEqual(data['last_name'], user.last_name)
        self.assertEqual(data['user_type'], User.TYPE_ADVISOR)
        self.assertEqual(data['school'], {
            u'id': school.id,
            u'registered': unicode(school.registered.isoformat()),
            u'name': unicode(school.name),
            u'address': unicode(school.address),
            u'city': unicode(school.city),
            u'state': unicode(school.state),
            u'zip_code': unicode(school.zip_code),
            u'country': unicode(school.country),
            u'primary_name': unicode(school.primary_name),
            u'primary_gender': school.primary_gender,
            u'primary_email': unicode(school.primary_email),
            u'primary_phone': unicode(school.primary_phone),
            u'primary_type': school.primary_type,
            u'secondary_name': unicode(school.secondary_name),
            u'secondary_gender': school.secondary_gender,
            u'secondary_email': unicode(school.secondary_email),
            u'secondary_phone': unicode(school.secondary_phone),
            u'secondary_type': school.secondary_type,
            u'program_type': school.program_type,
            u'times_attended': school.times_attended,
            u'international': school.international,
            u'waitlist': school.waitlist,
            u'beginner_delegates': school.beginner_delegates,
            u'intermediate_delegates': school.intermediate_delegates,
            u'advanced_delegates': school.advanced_delegates,
            u'spanish_speaking_delegates': school.spanish_speaking_delegates,
            u'chinese_speaking_delegates': school.chinese_speaking_delegates,
            u'countrypreferences': school.country_preference_ids,
            u'committeepreferences': list(school.committeepreferences.all()),
            u'registration_comments': unicode(school.registration_comments),
            u'fees_owed': float(school.fees_owed),
            u'fees_paid': float(school.fees_paid),
            u'assignments_finalized': school.assignments_finalized,
            u'delegate_names_finalized': school.delegate_names_finalized,
        })
