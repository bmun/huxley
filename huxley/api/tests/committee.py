from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.core.models import Committee
from huxley.utils.test import TestCommittee

import json
import unittest

class CommitteeDetailTestCase(unittest.TestCase):
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
        self.assertEqual(data['delegation_size'], 20)
        self.assertEqual(data['special'], True)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['full_name'], u'testCommittee')
        self.assertEqual(data['name'], u'IAmATestCommittee')

