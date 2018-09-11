# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models


class SecretariatMemberDetailGetTestCase(tests.RetrieveAPITestCase):
    '''Tests to see that anyone can retrieve secretariat member detail information'''
    url_name = "api:secretariat_member_detail"

    def setUp(self):
        self.name = "Shayna"
        self.is_head_chair = True
        self.committee = models.new_committee()
        self.sm1 = models.new_secretariat_member(
            name=self.name,
            committee=self.committee,
            is_head_chair=self.is_head_chair)

    def test_anonymous_user(self):
        '''Tests anonymous user can get secretariat information'''
        response = self.get_response(self.sm1.id)
        response.data.pop('id')
        self.assertEqual(response.data, {
            'name': self.name,
            'committee': self.committee.id,
            'is_head_chair': self.is_head_chair
        })

    def test_delegate(self):
        '''Tests delegate can get secretariat information'''
        self.assignment = models.new_assignment()
        self.user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE,
            assignment=self.assignment, )
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.sm1.id)
        response.data.pop('id')
        self.assertEqual(response.data, {
            'name': self.name,
            'committee': self.committee.id,
            'is_head_chair': self.is_head_chair
        })

    def test_chair(self):
        '''Tests chair can get secretariat information'''
        self.user = models.new_user(
            username='chair',
            password='chair',
            user_type=User.TYPE_CHAIR,
            committee_id=self.committee.id, )
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.sm1.id)
        response.data.pop('id')
        self.assertEqual(response.data, {
            'name': self.name,
            'committee': self.committee.id,
            'is_head_chair': self.is_head_chair
        })

    def test_advisor(self):
        '''Tests advisor can get secretariat information'''
        self.user = models.new_user(
            username='advisor',
            password='advisor',
            user_type=User.TYPE_ADVISOR, )
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.sm1.id)
        response.data.pop('id')
        self.assertEqual(response.data, {
            'name': self.name,
            'committee': self.committee.id,
            'is_head_chair': self.is_head_chair
        })

    def test_superuser(self):
        '''Tests superuser can get secretariat information'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response(self.sm1.id)
        response.data.pop('id')
        self.assertEqual(response.data, {
            'name': self.name,
            'committee': self.committee.id,
            'is_head_chair': self.is_head_chair
        })


class SecretariatMemberListGetTestCase(tests.ListAPITestCase):
    '''Tests to see that anyone can retrieve secretariat member list information'''
    url_name = "api:secretariat_member_list"

    def setUp(self):
        self.name1 = "Shayna"
        self.is_head_chair1 = True
        self.committee1 = models.new_committee()
        self.name2 = "AD"
        self.is_head_chair2 = False
        self.committee2 = models.new_committee()
        self.sm1 = models.new_secretariat_member(
            name=self.name1,
            committee=self.committee1,
            is_head_chair=self.is_head_chair1)
        self.sm2 = models.new_secretariat_member(
            name=self.name2, committee=self.committee2)

    def test_anonymous_user(self):
        '''Tests anonymous user can get secretariat information'''
        response = self.get_response()
        self.assertEqual(response.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])

    def test_delegate(self):
        '''Tests delegate can get secretariat information'''
        self.assignment = models.new_assignment()
        self.user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE,
            assignment=self.assignment, )
        self.client.login(username='delegate', password='delegate')
        response = self.get_response()
        self.assertEqual(response.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])

    def test_chair(self):
        '''Tests chair can get secretariat information'''
        self.chair_committee = models.new_committee()
        self.user = models.new_user(
            username='chair',
            password='chair',
            user_type=User.TYPE_CHAIR,
            committee_id=self.chair_committee.id, )
        self.client.login(username='chair', password='chair')
        response = self.get_response()
        self.assertEqual(response.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])

    def test_advisor(self):
        '''Tests advisor can get secretariat information'''
        self.user = models.new_user(
            username='advisor',
            password='advisor',
            user_type=User.TYPE_ADVISOR, )
        self.client.login(username='advisor', password='advisor')
        response = self.get_response()
        self.assertEqual(response.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])

    def test_superuser(self):
        '''Tests superuser can get secretariat information'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response()
        self.assertEqual(response.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])


class SecretariatMemberCommitteeListGetTestCase(tests.ListAPITestCase):
    '''Tests to see that anyone can retrieve secretariat member list information'''
    url_name = "api:secretariat_member_committee_list"

    def setUp(self):
        self.name1 = "Shayna"
        self.is_head_chair1 = True
        self.committee1 = models.new_committee()
        self.name2 = "AD"
        self.is_head_chair2 = False
        self.committee2 = models.new_committee()
        self.name3 = "Michael"
        self.is_head_chair3 = False
        self.empty_committee = models.new_committee()
        self.sm1 = models.new_secretariat_member(
            name=self.name1,
            committee=self.committee1,
            is_head_chair=self.is_head_chair1)
        self.sm2 = models.new_secretariat_member(
            name=self.name2, committee=self.committee2)
        self.sm3 = models.new_secretariat_member(
            name=self.name3,
            committee=self.committee1,
            is_head_chair=self.is_head_chair3)

    def test_anonymous_user(self):
        '''Tests anonymous user can get secretariat information'''
        response1 = self.get_response()
        self.assertEqual(response1.data, [])

        params2 = {'committee_id': self.empty_committee.id}
        response2 = self.get_response(params=params2)
        self.assertEqual(response2.data, [])

        params3 = {'committee_id': self.committee1.id}
        response3 = self.get_response(params=params3)
        self.assertEqual(response3.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm3.id,
                'name': self.name3,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair3
            }
        ])

        params4 = {'committee_id': self.committee2.id}
        resposne4 = self.get_response(params=params4)
        self.assertEqual(resposne4.data, [
            {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])

    def test_delegate(self):
        '''Tests delegate can get secretariat information'''
        self.assignment = models.new_assignment()
        self.user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE,
            assignment=self.assignment, )
        self.client.login(username='delegate', password='delegate')
        response1 = self.get_response()
        self.assertEqual(response1.data, [])

        params2 = {'committee_id': self.empty_committee.id}
        response2 = self.get_response(params=params2)
        self.assertEqual(response2.data, [])

        params3 = {'committee_id': self.committee1.id}
        response3 = self.get_response(params=params3)
        self.assertEqual(response3.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm3.id,
                'name': self.name3,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair3
            }
        ])

        params4 = {'committee_id': self.committee2.id}
        resposne4 = self.get_response(params=params4)
        self.assertEqual(resposne4.data, [
            {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])

    def test_chair(self):
        '''Tests chair can get secretariat information'''
        self.chair_committee = models.new_committee()
        self.user = models.new_user(
            username='chair',
            password='chair',
            user_type=User.TYPE_CHAIR,
            committee_id=self.chair_committee.id, )
        self.client.login(username='chair', password='chair')
        response1 = self.get_response()
        self.assertEqual(response1.data, [])

        params2 = {'committee_id': self.empty_committee.id}
        response2 = self.get_response(params=params2)
        self.assertEqual(response2.data, [])

        params3 = {'committee_id': self.committee1.id}
        response3 = self.get_response(params=params3)
        self.assertEqual(response3.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm3.id,
                'name': self.name3,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair3
            }
        ])

        params4 = {'committee_id': self.committee2.id}
        resposne4 = self.get_response(params=params4)
        self.assertEqual(resposne4.data, [
            {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])

    def test_advisor(self):
        '''Tests advisor can get secretariat information'''
        self.user = models.new_user(
            username='advisor',
            password='advisor',
            user_type=User.TYPE_ADVISOR, )
        self.client.login(username='advisor', password='advisor')
        response1 = self.get_response()
        self.assertEqual(response1.data, [])

        params2 = {'committee_id': self.empty_committee.id}
        response2 = self.get_response(params=params2)
        self.assertEqual(response2.data, [])

        params3 = {'committee_id': self.committee1.id}
        response3 = self.get_response(params=params3)
        self.assertEqual(response3.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm3.id,
                'name': self.name3,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair3
            }
        ])

        params4 = {'committee_id': self.committee2.id}
        resposne4 = self.get_response(params=params4)
        self.assertEqual(resposne4.data, [
            {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])

    def test_superuser(self):
        '''Tests superuser can get secretariat information'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response1 = self.get_response()
        self.assertEqual(response1.data, [])

        params2 = {'committee_id': self.empty_committee.id}
        response2 = self.get_response(params=params2)
        self.assertEqual(response2.data, [])

        params3 = {'committee_id': self.committee1.id}
        response3 = self.get_response(params=params3)
        self.assertEqual(response3.data, [
            {
                'id': self.sm1.id,
                'name': self.name1,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair1
            }, {
                'id': self.sm3.id,
                'name': self.name3,
                'committee': self.committee1.id,
                'is_head_chair': self.is_head_chair3
            }
        ])

        params4 = {'committee_id': self.committee2.id}
        resposne4 = self.get_response(params=params4)
        self.assertEqual(resposne4.data, [
            {
                'id': self.sm2.id,
                'name': self.name2,
                'committee': self.committee2.id,
                'is_head_chair': self.is_head_chair2
            }
        ])
