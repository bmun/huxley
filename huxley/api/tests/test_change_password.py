# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.accounts.models import User
from huxley.api.tests import UpdateAPITestCase
from huxley.utils.test import TestUsers


class ChangePasswordTestCase(UpdateAPITestCase):
    url_name = 'api:user_password'
    is_resource = False
    params = {'password': 'hello',
              'new_password': 'world'}

    def setUp(self):
        self.user = TestUsers.new_user(username='hello', password='hello')

    def test_anonymous_user(self):
        '''It should not allow anonymous users to change passwords.'''
        response = self.get_response()
        self.assertPermissionDenied(response)

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('hello'))

    def test_self(self):
        '''Users should be able to change their passwords.'''
        self.client.login(username='hello', password='hello')

        response = self.get_response()
        self.assertOK(response)

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('world'))

    def test_incorrect_password(self):
        '''It should reject the request if given an incorrect password.'''
        self.client.login(username='hello', password='hello')
        params = self.get_params(password='incorrect')

        response = self.get_response(params=params)
        self.assertAuthenticationFailed(response)

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('hello'))
