# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.utils.test import TestSchools

import json

class SchoolDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, school_id):
        return reverse('api:school_detail', args=(school_id,))

    def get_response(self, url):
        return json.loads(self.client.get(url).content)

    def test_anonymous_user(self):
        '''It should reject request from an anonymous user.'''
        school = TestSchools.new_school()
        url = self.get_url(school.id)
        data = self.get_response(url)

        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'],
                         u'Authentication credentials were not provided.')
