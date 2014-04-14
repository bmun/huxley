# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.accounts.models import HuxleyUser
from huxley.utils.test import TestUsers

import json
import unittest

class UserDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, user_id):
        return reverse('api:user_detail', args=(user_id,))

    def get_response(self, url):
        return json.loads(self.client.get(url).content)

    def test_sanity(self):
        '''It should return the correct fields for a single user.'''
        user = TestUsers.new_user(username='lol', password='lol', school_id=1)
        url = self.get_url(user.id)

        data = self.get_response(url)
        self.assertEquals(
            data['detail'],
            u'Authentication credentials were not provided.')

        self.client.login(username='lol', password='lol')
        data = self.get_response(url)

        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['first_name'], user.first_name)
        self.assertEqual(data['last_name'], user.last_name)
        self.assertEqual(data['user_type'], HuxleyUser.TYPE_ADVISOR)
        self.assertEqual(data['school'], user.school_id)
        self.assertEqual(data['committee'], user.committee_id)

