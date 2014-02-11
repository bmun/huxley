from django.test import TestCase
from django.test.client import Client

from huxley.accounts.models import HuxleyUser

import json
import unittest

class UserDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sanity(self):
        '''It should return the correct fields for a single user.'''
        user = HuxleyUser.objects.create_user(username='kunal',
                                              email='kunal@lol.com',
                                              password='helloworld')
        user.first_name = 'Kunal'
        user.last_name = 'Mehta'
        user.school_id = 1
        user.save()

        response = self.client.get('/api/users/%d' % user.id)
        data = json.loads(response.content)

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['first_name'], 'Kunal')
        self.assertEqual(data['last_name'], 'Mehta')
        self.assertEqual(data['user_type'], HuxleyUser.TYPE_ADVISOR)
        self.assertEqual(data['school'], 1)
        self.assertEqual(data['committee'], None)

