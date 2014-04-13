from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.core.models import Committee
from huxley.utils.test import TestCommittee

import json
import unittest

class CommitteeDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_url(self, committee_id):
        return reverse('api:committee_detail', args=(committee_id,))

    def get_response(self, url):
        return json.loads(self.client.get(url).content)

    def test_sanity(self):
        '''It should return the correct fields for a committee.'''
        committee = TestCommittee.new_committee(name="IAmATestCommittee", delegation_size=20, special=True)
        url = self.get_url(committee.id)

        data = self.get_response(url)
        self.assertEquals(
            data['detail'],
            u'Authentication credentials were not provided.')

