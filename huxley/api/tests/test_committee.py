# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.utils.test import TestCommittees


class CommitteeDetailGetTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, committee_id):
        return reverse('api:committee_detail', args=(committee_id,))

    def get_response(self, url):
        return json.loads(self.client.get(url).content)

    def test_anonymous_user(self):
        '''It should return the correct fields for a committee.'''
        c = TestCommittees.new_committee()
        url = self.get_url(c.id)

        data = self.get_response(url)
        self.assertEqual(data['delegation_size'], c.delegation_size)
        self.assertEqual(data['special'], c.special)
        self.assertEqual(data['id'], c.id)
        self.assertEqual(data['full_name'], c.full_name)
        self.assertEqual(data['name'], c.name)
