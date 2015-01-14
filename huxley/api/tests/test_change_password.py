# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.accounts.exceptions import PasswordChangeFailed
from huxley.accounts.models import User
from huxley.api.tests import UpdateAPITestCase
from huxley.utils.test import TestUsers


class ChangePasswordTestCase(UpdateAPITestCase):
    url_name = 'api:user_password'
    is_resource = False
    params = {'password': 'old&busted',
              'new_password': 'newhotness'}

    def setUp(self):
        self.user = TestUsers.new_user(username='old&busted',
                                       password='old&busted')

    def login(self):
        self.client.login(username='old&busted', password='old&busted')

    def test_anonymous_user(self):
        '''It should not allow anonymous users to change passwords.'''
        response = self.get_response()
        self.assertPermissionDenied(response)

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('old&busted'))

    def test_self(self):
        '''Users should be able to change their passwords.'''
        self.login()

        response = self.get_response()
        self.assertOK(response)

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('newhotness'))

    def test_missing_fields(self):
        '''It should reject the request if there are missing fields.'''
        self.login()
        params = self.get_params(new_password='')

        response = self.get_response(params=params)
        self.assertEqual(response.data, {
            'detail': PasswordChangeFailed.MISSING_FIELDS})

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('old&busted'))

        params = self.get_params(password='')
        response = self.get_response(params=params)
        self.assertEqual(response.data, {
            'detail': PasswordChangeFailed.MISSING_FIELDS})

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('old&busted'))

    def test_short_password(self):
        '''It should reject the request if given a short password.'''
        self.login()
        params = self.get_params(new_password='a')

        response = self.get_response(params=params)
        self.assertEqual(response.data, {
            'detail': PasswordChangeFailed.PASSWORD_TOO_SHORT})

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('old&busted'))

    def test_invalid_password(self):
        '''It should reject the request if given an invalid password.'''
        self.login()
        params = self.get_params(new_password='invalid>hotness')

        response = self.get_response(params=params)
        self.assertEqual(response.data, {
            'detail': PasswordChangeFailed.INVALID_CHARACTERS})

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('old&busted'))

    def test_incorrect_password(self):
        '''It should reject the request if given an incorrect password.'''
        self.login()
        params = self.get_params(password='incorrect')

        response = self.get_response(params=params)
        self.assertEqual(response.data, {
            'detail': PasswordChangeFailed.INCORRECT_PASSWORD})

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('old&busted'))
