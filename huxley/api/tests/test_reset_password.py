# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import status

from huxley.api.tests import CreateAPITestCase
from huxley.utils.test import TestUsers


class ResetPasswordTestCase(CreateAPITestCase):
    url_name = 'api:user_password'
    is_resource = False
    params = {'username': 'mikejones'}

    def setUp(self):
        self.user = TestUsers.new_user(username='mikejones', email='who@mj.com')

    def test_username(self):
        response = self.get_response()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_email(self):
        params = self.get_params(username='who@mj.com')
        response = self.get_response(params=params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_nonexistant(self):
        params = self.get_params(username='nobody')
        response = self.get_response(params=params)
        self.assertNotFound(response)
