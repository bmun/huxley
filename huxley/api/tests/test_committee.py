# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.api.tests import GetAPITestCase
from huxley.utils.test import TestCommittees


class CommitteeDetailGetTestCase(GetAPITestCase):
    url_name = 'api:committee_detail'

    def test_anonymous_user(self):
        '''It should return the correct fields for a committee.'''
        c = TestCommittees.new_committee()
        data = self.get_response(c.id)
        self.assertEqual(data, {'id': c.id,
                                'name': c.name,
                                'full_name': c.full_name,
                                'delegation_size': c.delegation_size,
                                'special': c.special})
