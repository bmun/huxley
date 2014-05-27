# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from huxley.utils.test import TestSchools, TestUsers
from huxley.api.tests import GetAPITestCase


class SchoolDetailGetTestCase(GetAPITestCase):
    url_name = 'api:school_detail'

    def test_anonymous_user(self):
        '''It should reject request from an anonymous user.'''
        school = TestSchools.new_school()
        data = self.get_response(school.id)

        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['detail'],
                         u'Authentication credentials were not provided.')

    def test_self(self):
        '''It should allow the get request from the user.'''
        school = TestSchools.new_school()
        user = TestUsers.objects.get(school=school)
        data = self.get_response(school.id)

        self.client.login(username='user', password='user')



class SchoolDetailPutTestCase(TestCase):
    pass

class SchoolDetailPatchTestCase(TestCase):
    pass

class SchoolDetailDeleteTestCase(TestCase):
    pass

class SchoolListGetTestCase(TestCase):
    pass

class SchoolListPostTestCase(TestCase):
    pass

