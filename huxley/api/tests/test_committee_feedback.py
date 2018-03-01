# copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.exceptions import ValidationError

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models
import random


class CommitteeFeedbackDetailCreateTestCase(tests.CreateAPITestCase):
    url_name = 'api:committee_feedback_create'

    def setUp(self):
        self.committee_1 = models.new_committee(name='CYBER')
        self.committee_2 = models.new_committee(name='UNPBC')
        self.assignment_1 = models.new_assignment(committee=self.committee_1)
        self.assignment_2 = models.new_assignment(committee=self.committee_2)
        self.delegate_1 = models.new_delegate(assignment=self.assignment_1)
        self.delegate_2 = models.new_delegate(assignment=self.assignment_2)
        self.params = {
            'comment': "I never got called on ever. SAD!",
            'committee': self.committee_1.id,
            'rating': 4,
            'chair_1_name': "Jake Tibbetts",
            'chair_1_comment': "He was the head chair",
            'chair_1_rating': 10,
            'chair_2_name': "Trent",
            'chair_2_comment': "He was the funny one",
            'chair_2_rating': 3,
            'chair_3_name': "Suchi",
            'chair_3_comment': "She was the cute one",
            'chair_3_rating': 8,
            'chair_4_name': "Nikhil",
            'chair_4_comment': "He was the baby",
            'chair_4_rating': 1,
            'chair_5_name': "",
            'chair_5_comment': "",
            'chair_5_rating': 0,
            'chair_6_name': "",
            'chair_6_comment': "",
            'chair_6_rating': 0,
            'chair_7_name': "",
            'chair_7_comment': "",
            'chair_7_rating': 0,
            'chair_8_name': "",
            'chair_8_comment': "",
            'chair_8_rating': 0,
            'chair_9_name': "",
            'chair_9_comment': "",
            'chair_9_rating': 0,
            'chair_10_name': "",
            'chair_10_comment': "",
            'chair_10_rating': 0
        }

    def test_anonymous_user(self):
        '''Anonymous users cannot create feedback'''
        response = self.get_response(params=self.params)
        self.assertNotAuthenticated(response)

    def test_delegate(self):
        '''Delegate can create feedback only once 
           for the committee they are in'''
        self.user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE,
            delegate=self.delegate_1,
            assignment=self.assignment_1)
        self.client.login(username='delegate', password='delegate')
        self.assertFalse(self.user.delegate.committee_feedback_submitted)
        self.params_fail = {
            'comment': "Fail Test",
            'committee': self.committee_2.id
        }
        response_0 = self.get_response(params=self.params_fail)
        self.assertPermissionDenied(response_0)
        response_1 = self.get_response(params=self.params)
        response_1.data.pop('id')
        self.assertEqual(response_1.data, {
            "committee": self.committee_1.id,
            "comment": self.params['comment'],
            'rating': self.params['rating'],
            'chair_1_name': self.params['chair_1_name'],
            'chair_1_comment': self.params['chair_1_comment'],
            'chair_1_rating': self.params['chair_1_rating'],
            'chair_2_name': self.params['chair_2_name'],
            'chair_2_comment': self.params['chair_2_comment'],
            'chair_2_rating': self.params['chair_2_rating'],
            'chair_3_name': self.params['chair_3_name'],
            'chair_3_comment': self.params['chair_3_comment'],
            'chair_3_rating': self.params['chair_3_rating'],
            'chair_4_name': self.params['chair_4_name'],
            'chair_4_comment': self.params['chair_4_comment'],
            'chair_4_rating': self.params['chair_4_rating'],
            'chair_5_name': self.params['chair_5_name'],
            'chair_5_comment': self.params['chair_5_comment'],
            'chair_5_rating': self.params['chair_5_rating'],
            'chair_6_name': self.params['chair_6_name'],
            'chair_6_comment': self.params['chair_6_comment'],
            'chair_6_rating': self.params['chair_6_rating'],
            'chair_7_name': self.params['chair_7_name'],
            'chair_7_comment': self.params['chair_7_comment'],
            'chair_7_rating': self.params['chair_7_rating'],
            'chair_8_name': self.params['chair_8_name'],
            'chair_8_comment': self.params['chair_8_comment'],
            'chair_8_rating': self.params['chair_8_rating'],
            'chair_9_name': self.params['chair_9_name'],
            'chair_9_comment': self.params['chair_9_comment'],
            'chair_9_rating': self.params['chair_9_rating'],
            'chair_10_name': self.params['chair_10_name'],
            'chair_10_comment': self.params['chair_10_comment'],
            'chair_10_rating': self.params['chair_10_rating'],
        })
        self.user.delegate.refresh_from_db()
        self.assertTrue(self.user.delegate.committee_feedback_submitted)
        response_2 = self.get_response(params=self.params)
        self.assertPermissionDenied(response_2)

    def test_chair(self):
        '''Chair cannot create committee feedback'''
        self.user = models.new_user(
            username='chair',
            password='chair',
            user_type=User.TYPE_CHAIR,
            committee=self.committee_1)
        self.client.login(username='chair', password='chair')
        response = self.get_response(params=self.params)
        self.assertPermissionDenied(response)

    def test_advisor(self):
        '''Advisor cannot create committee feedback'''
        self.user = models.new_user(
            username='advisor',
            password='advisor',
            user_type=User.TYPE_ADVISOR, )
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(params=self.params)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''Superuser can create feedback'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response(params=self.params)
        response.data.pop('id')
        self.assertEqual(response.data, {
            "committee": self.committee_1.id,
            "comment": self.params['comment'],
            'rating': self.params['rating'],
            'chair_1_name': self.params['chair_1_name'],
            'chair_1_comment': self.params['chair_1_comment'],
            'chair_1_rating': self.params['chair_1_rating'],
            'chair_2_name': self.params['chair_2_name'],
            'chair_2_comment': self.params['chair_2_comment'],
            'chair_2_rating': self.params['chair_2_rating'],
            'chair_3_name': self.params['chair_3_name'],
            'chair_3_comment': self.params['chair_3_comment'],
            'chair_3_rating': self.params['chair_3_rating'],
            'chair_4_name': self.params['chair_4_name'],
            'chair_4_comment': self.params['chair_4_comment'],
            'chair_4_rating': self.params['chair_4_rating'],
            'chair_5_name': self.params['chair_5_name'],
            'chair_5_comment': self.params['chair_5_comment'],
            'chair_5_rating': self.params['chair_5_rating'],
            'chair_6_name': self.params['chair_6_name'],
            'chair_6_comment': self.params['chair_6_comment'],
            'chair_6_rating': self.params['chair_6_rating'],
            'chair_7_name': self.params['chair_7_name'],
            'chair_7_comment': self.params['chair_7_comment'],
            'chair_7_rating': self.params['chair_7_rating'],
            'chair_8_name': self.params['chair_8_name'],
            'chair_8_comment': self.params['chair_8_comment'],
            'chair_8_rating': self.params['chair_8_rating'],
            'chair_9_name': self.params['chair_9_name'],
            'chair_9_comment': self.params['chair_9_comment'],
            'chair_9_rating': self.params['chair_9_rating'],
            'chair_10_name': self.params['chair_10_name'],
            'chair_10_comment': self.params['chair_10_comment'],
            'chair_10_rating': self.params['chair_10_rating'],
        })

    def test_invalid_data(self):
        '''Valid user cannot send invalid data'''
        self.user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE,
            delegate=self.delegate_2,
            assignment=self.assignment_2)
        self.client.login(username='delegate', password='delegate')
        self.assertFalse(self.user.delegate.committee_feedback_submitted)
        self.bad_params = {
            'comment': "Wow what a great comment!",
            'committee': self.committee_2.id,
            'rating': -1,
            'chair_1_name': "Hacky McHacker",
            'chair_1_comment':
            "I come up with great test case comments hacking late at night",
            'chair_1_rating': -30,
            'chair_2_name': "The Spirit of California",
            'chair_2_comment':
            ";DROP TABLE ... haha jk I have no clue how to do SQL injection",
            'chair_2_rating': 4,
            'chair_3_name': "Nickelback",
            'chair_3_comment': "LOOK AT THIS GRAAAAAAPH",
            'chair_3_rating': 156,
            'chair_4_name': "",
            'chair_4_comment': "",
            'chair_4_rating': 0,
            'chair_5_name': "",
            'chair_5_comment': "",
            'chair_5_rating': 0,
            'chair_6_name': "",
            'chair_6_comment': "",
            'chair_6_rating': 0,
            'chair_7_name': "",
            'chair_7_comment': "",
            'chair_7_rating': 0,
            'chair_8_name': "",
            'chair_8_comment': "",
            'chair_8_rating': 0,
            'chair_9_name': "",
            'chair_9_comment': "",
            'chair_9_rating': 0,
            'chair_10_name': "",
            'chair_10_comment': "",
            'chair_10_rating': 0,
        }
        response = self.get_response(params=self.bad_params)
        bad_fields = ['rating', 'chair_1_rating', 'chair_3_rating']
        self.assertInvalidCommitteeRating(response, bad_fields,
                                          self.bad_params)


class CommitteeFeedbackDetailGetTestCase(tests.RetrieveAPITestCase):
    url_name = 'api:committee_feedback_detail'

    def setUp(self):
        self.committee_1 = models.new_committee(name='UNSC')
        self.committee_2 = models.new_committee(name='HSC')
        self.params1 = {
            'comment': "I never got called on ever. SAD!",
            'rating': 4,
            'chair_1_name': "Jake Tibbetts",
            'chair_1_comment': "He was the head chair",
            'chair_1_rating': 10,
            'chair_2_name': "Trent",
            'chair_2_comment': "He was the funny one",
            'chair_2_rating': 3,
            'chair_3_name': "Suchi",
            'chair_3_comment': "She was the cute one",
            'chair_3_rating': 8,
            'chair_4_name': "Nikhil",
            'chair_4_comment': "He was the baby",
            'chair_4_rating': 1,
            'chair_5_name': "",
            'chair_5_comment': "",
            'chair_5_rating': 0,
            'chair_6_name': "",
            'chair_6_comment': "",
            'chair_6_rating': 0,
            'chair_7_name': "",
            'chair_7_comment': "",
            'chair_7_rating': 0,
            'chair_8_name': "",
            'chair_8_comment': "",
            'chair_8_rating': 0,
            'chair_9_name': "",
            'chair_9_comment': "",
            'chair_9_rating': 0,
            'chair_10_name': "",
            'chair_10_comment': "",
            'chair_10_rating': 0
        }

        self.params2 = {
            'comment': "Not Good",
            'rating': 3,
            'chair_1_name': "Jak Tibetts",
            'chair_1_comment': "He was a literal chair",
            'chair_1_rating': 8,
            'chair_2_name': "Tent Gumberg",
            'chair_2_comment': "He was the gummy one",
            'chair_2_rating': 4,
            'chair_3_name': "Suchi Luchi",
            'chair_3_comment': "She was the muchi one",
            'chair_3_rating': 6,
            'chair_4_name': "Nikhil the pill",
            'chair_4_comment': "He was the still just the baby",
            'chair_4_rating': 2,
            'chair_5_name': "",
            'chair_5_comment': "",
            'chair_5_rating': 0,
            'chair_6_name': "",
            'chair_6_comment': "",
            'chair_6_rating': 0,
            'chair_7_name': "",
            'chair_7_comment': "",
            'chair_7_rating': 0,
            'chair_8_name': "",
            'chair_8_comment': "",
            'chair_8_rating': 0,
            'chair_9_name': "",
            'chair_9_comment': "",
            'chair_9_rating': 0,
            'chair_10_name': "",
            'chair_10_comment': "",
            'chair_10_rating': 0
        }

        self.feedback_1 = models.new_committee_feedback(
            committee=self.committee_1,
            comment=self.params1['comment'],
            rating=self.params1['rating'],
            chair_1_name=self.params1['chair_1_name'],
            chair_1_comment=self.params1['chair_1_comment'],
            chair_1_rating=self.params1['chair_1_rating'],
            chair_2_name=self.params1['chair_2_name'],
            chair_2_comment=self.params1['chair_2_comment'],
            chair_2_rating=self.params1['chair_2_rating'],
            chair_3_name=self.params1['chair_3_name'],
            chair_3_comment=self.params1['chair_3_comment'],
            chair_3_rating=self.params1['chair_3_rating'],
            chair_4_name=self.params1['chair_4_name'],
            chair_4_comment=self.params1['chair_4_comment'],
            chair_4_rating=self.params1['chair_4_rating'],
            chair_5_name=self.params1['chair_5_name'],
            chair_5_comment=self.params1['chair_5_comment'],
            chair_5_rating=self.params1['chair_5_rating'],
            chair_6_name=self.params1['chair_6_name'],
            chair_6_comment=self.params1['chair_6_comment'],
            chair_6_rating=self.params1['chair_6_rating'],
            chair_7_name=self.params1['chair_7_name'],
            chair_7_comment=self.params1['chair_7_comment'],
            chair_7_rating=self.params1['chair_7_rating'],
            chair_8_name=self.params1['chair_8_name'],
            chair_8_comment=self.params1['chair_8_comment'],
            chair_8_rating=self.params1['chair_8_rating'],
            chair_9_name=self.params1['chair_9_name'],
            chair_9_comment=self.params1['chair_9_comment'],
            chair_9_rating=self.params1['chair_9_rating'],
            chair_10_name=self.params1['chair_10_name'],
            chair_10_comment=self.params1['chair_10_comment'],
            chair_10_rating=self.params1['chair_10_rating'])

        self.feedback_2 = models.new_committee_feedback(
            committee=self.committee_2,
            comment=self.params2['comment'],
            rating=self.params2['rating'],
            chair_1_name=self.params2['chair_1_name'],
            chair_1_comment=self.params2['chair_1_comment'],
            chair_1_rating=self.params2['chair_1_rating'],
            chair_2_name=self.params2['chair_2_name'],
            chair_2_comment=self.params2['chair_2_comment'],
            chair_2_rating=self.params2['chair_2_rating'],
            chair_3_name=self.params2['chair_3_name'],
            chair_3_comment=self.params2['chair_3_comment'],
            chair_3_rating=self.params2['chair_3_rating'],
            chair_4_name=self.params2['chair_4_name'],
            chair_4_comment=self.params2['chair_4_comment'],
            chair_4_rating=self.params2['chair_4_rating'],
            chair_5_name=self.params2['chair_5_name'],
            chair_5_comment=self.params2['chair_5_comment'],
            chair_5_rating=self.params2['chair_5_rating'],
            chair_6_name=self.params2['chair_6_name'],
            chair_6_comment=self.params2['chair_6_comment'],
            chair_6_rating=self.params2['chair_6_rating'],
            chair_7_name=self.params2['chair_7_name'],
            chair_7_comment=self.params2['chair_7_comment'],
            chair_7_rating=self.params2['chair_7_rating'],
            chair_8_name=self.params2['chair_8_name'],
            chair_8_comment=self.params2['chair_8_comment'],
            chair_8_rating=self.params2['chair_8_rating'],
            chair_9_name=self.params2['chair_9_name'],
            chair_9_comment=self.params2['chair_9_comment'],
            chair_9_rating=self.params2['chair_9_rating'],
            chair_10_name=self.params2['chair_10_name'],
            chair_10_comment=self.params2['chair_10_comment'],
            chair_10_rating=self.params2['chair_10_rating'])
        self.assignment_1 = models.new_assignment(committee=self.committee_1)

    def test_anonymous_user(self):
        '''Anonymous User cannot retrieve feedback'''
        response = self.get_response(self.feedback_1.id)
        self.assertNotAuthenticated(response)

    def test_delegate(self):
        '''Delegate cannot retrieve feedback, even their own because 
        of anonymity.'''
        self.user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE,
            assignment=self.assignment_1, )
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.feedback_1.id)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Chair can retrieve feedback from only their own committee'''
        self.user = models.new_user(
            username='chair',
            password='chair',
            user_type=User.TYPE_CHAIR,
            committee_id=self.committee_1.id, )
        self.client.login(username='chair', password='chair')
        response_1 = self.get_response(self.feedback_1.id)
        response_1.data.pop('id')
        self.assertEqual(response_1.data, {
            'committee': self.committee_1.id,
            'comment': self.feedback_1.comment,
            'rating': self.feedback_1.rating,
            'chair_1_name': self.feedback_1.chair_1_name,
            'chair_1_comment': self.feedback_1.chair_1_comment,
            'chair_1_rating': self.feedback_1.chair_1_rating,
            'chair_2_name': self.feedback_1.chair_2_name,
            'chair_2_comment': self.feedback_1.chair_2_comment,
            'chair_2_rating': self.feedback_1.chair_2_rating,
            'chair_3_name': self.feedback_1.chair_3_name,
            'chair_3_comment': self.feedback_1.chair_3_comment,
            'chair_3_rating': self.feedback_1.chair_3_rating,
            'chair_4_name': self.feedback_1.chair_4_name,
            'chair_4_comment': self.feedback_1.chair_4_comment,
            'chair_4_rating': self.feedback_1.chair_4_rating,
            'chair_5_name': self.feedback_1.chair_5_name,
            'chair_5_comment': self.feedback_1.chair_5_comment,
            'chair_5_rating': self.feedback_1.chair_5_rating,
            'chair_6_name': self.feedback_1.chair_6_name,
            'chair_6_comment': self.feedback_1.chair_6_comment,
            'chair_6_rating': self.feedback_1.chair_6_rating,
            'chair_7_name': self.feedback_1.chair_7_name,
            'chair_7_comment': self.feedback_1.chair_7_comment,
            'chair_7_rating': self.feedback_1.chair_7_rating,
            'chair_8_name': self.feedback_1.chair_8_name,
            'chair_8_comment': self.feedback_1.chair_8_comment,
            'chair_8_rating': self.feedback_1.chair_8_rating,
            'chair_9_name': self.feedback_1.chair_9_name,
            'chair_9_comment': self.feedback_1.chair_9_comment,
            'chair_9_rating': self.feedback_1.chair_9_rating,
            'chair_10_name': self.feedback_1.chair_10_name,
            'chair_10_comment': self.feedback_1.chair_10_comment,
            'chair_10_rating': self.feedback_1.chair_10_rating
        })
        response_2 = self.get_response(self.feedback_2.id)
        self.assertPermissionDenied(response_2)

    def test_advisor(self):
        '''Advisor cannot retrieve feedback'''
        self.user = models.new_user(
            username='advisor',
            password='advisor',
            user_type=User.TYPE_ADVISOR, )
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.feedback_1.id)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''Superuser can retrieve any feedback'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response_1 = self.get_response(self.feedback_1.id)
        response_1.data.pop('id')
        self.assertEqual(response_1.data, {
            'committee': self.committee_1.id,
            'comment': self.feedback_1.comment,
            'rating': self.feedback_1.rating,
            'chair_1_name': self.feedback_1.chair_1_name,
            'chair_1_comment': self.feedback_1.chair_1_comment,
            'chair_1_rating': self.feedback_1.chair_1_rating,
            'chair_2_name': self.feedback_1.chair_2_name,
            'chair_2_comment': self.feedback_1.chair_2_comment,
            'chair_2_rating': self.feedback_1.chair_2_rating,
            'chair_3_name': self.feedback_1.chair_3_name,
            'chair_3_comment': self.feedback_1.chair_3_comment,
            'chair_3_rating': self.feedback_1.chair_3_rating,
            'chair_4_name': self.feedback_1.chair_4_name,
            'chair_4_comment': self.feedback_1.chair_4_comment,
            'chair_4_rating': self.feedback_1.chair_4_rating,
            'chair_5_name': self.feedback_1.chair_5_name,
            'chair_5_comment': self.feedback_1.chair_5_comment,
            'chair_5_rating': self.feedback_1.chair_5_rating,
            'chair_6_name': self.feedback_1.chair_6_name,
            'chair_6_comment': self.feedback_1.chair_6_comment,
            'chair_6_rating': self.feedback_1.chair_6_rating,
            'chair_7_name': self.feedback_1.chair_7_name,
            'chair_7_comment': self.feedback_1.chair_7_comment,
            'chair_7_rating': self.feedback_1.chair_7_rating,
            'chair_8_name': self.feedback_1.chair_8_name,
            'chair_8_comment': self.feedback_1.chair_8_comment,
            'chair_8_rating': self.feedback_1.chair_8_rating,
            'chair_9_name': self.feedback_1.chair_9_name,
            'chair_9_comment': self.feedback_1.chair_9_comment,
            'chair_9_rating': self.feedback_1.chair_9_rating,
            'chair_10_name': self.feedback_1.chair_10_name,
            'chair_10_comment': self.feedback_1.chair_10_comment,
            'chair_10_rating': self.feedback_1.chair_10_rating
        })
        response_2 = self.get_response(self.feedback_2.id)
        response_2.data.pop('id')
        self.assertEqual(response_2.data, {
            'committee': self.committee_2.id,
            'comment': self.feedback_2.comment,
            'rating': self.feedback_2.rating,
            'chair_1_name': self.feedback_2.chair_1_name,
            'chair_1_comment': self.feedback_2.chair_1_comment,
            'chair_1_rating': self.feedback_2.chair_1_rating,
            'chair_2_name': self.feedback_2.chair_2_name,
            'chair_2_comment': self.feedback_2.chair_2_comment,
            'chair_2_rating': self.feedback_2.chair_2_rating,
            'chair_3_name': self.feedback_2.chair_3_name,
            'chair_3_comment': self.feedback_2.chair_3_comment,
            'chair_3_rating': self.feedback_2.chair_3_rating,
            'chair_4_name': self.feedback_2.chair_4_name,
            'chair_4_comment': self.feedback_2.chair_4_comment,
            'chair_4_rating': self.feedback_2.chair_4_rating,
            'chair_5_name': self.feedback_2.chair_5_name,
            'chair_5_comment': self.feedback_2.chair_5_comment,
            'chair_5_rating': self.feedback_2.chair_5_rating,
            'chair_6_name': self.feedback_2.chair_6_name,
            'chair_6_comment': self.feedback_2.chair_6_comment,
            'chair_6_rating': self.feedback_2.chair_6_rating,
            'chair_7_name': self.feedback_2.chair_7_name,
            'chair_7_comment': self.feedback_2.chair_7_comment,
            'chair_7_rating': self.feedback_2.chair_7_rating,
            'chair_8_name': self.feedback_2.chair_8_name,
            'chair_8_comment': self.feedback_2.chair_8_comment,
            'chair_8_rating': self.feedback_2.chair_8_rating,
            'chair_9_name': self.feedback_2.chair_9_name,
            'chair_9_comment': self.feedback_2.chair_9_comment,
            'chair_9_rating': self.feedback_2.chair_9_rating,
            'chair_10_name': self.feedback_2.chair_10_name,
            'chair_10_comment': self.feedback_2.chair_10_comment,
            'chair_10_rating': self.feedback_2.chair_10_rating
        })


class CommitteeFeedbackListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:committee_feedback_list'

    def setUp(self):
        self.committee_1 = models.new_committee(name='DISC')
        self.committee_2 = models.new_committee(name='SOCHUM')

        self.params1 = {
            'comment': "I never got called on ever. SAD!",
            'rating': 4,
            'chair_1_name': "Jake Tibbetts",
            'chair_1_comment': "He was the head chair",
            'chair_1_rating': 10,
            'chair_2_name': "Trent",
            'chair_2_comment': "He was the funny one",
            'chair_2_rating': 3,
            'chair_3_name': "Suchi",
            'chair_3_comment': "She was the cute one",
            'chair_3_rating': 8,
            'chair_4_name': "Nikhil",
            'chair_4_comment': "He was the baby",
            'chair_4_rating': 1,
            'chair_5_name': "",
            'chair_5_comment': "",
            'chair_5_rating': 0,
            'chair_6_name': "",
            'chair_6_comment': "",
            'chair_6_rating': 0,
            'chair_7_name': "",
            'chair_7_comment': "",
            'chair_7_rating': 0,
            'chair_8_name': "",
            'chair_8_comment': "",
            'chair_8_rating': 0,
            'chair_9_name': "",
            'chair_9_comment': "",
            'chair_9_rating': 0,
            'chair_10_name': "",
            'chair_10_comment': "",
            'chair_10_rating': 0
        }

        self.params2 = {
            'comment': "Not Good",
            'rating': 3,
            'chair_1_name': "Jak Tibetts",
            'chair_1_comment': "He was a literal chair",
            'chair_1_rating': 8,
            'chair_2_name': "Tent Gumberg",
            'chair_2_comment': "He was the gummy one",
            'chair_2_rating': 4,
            'chair_3_name': "Suchi Luchi",
            'chair_3_comment': "She was the muchi one",
            'chair_3_rating': 6,
            'chair_4_name': "Nikhil the pill",
            'chair_4_comment': "He was the still just the baby",
            'chair_4_rating': 2,
            'chair_5_name': "",
            'chair_5_comment': "",
            'chair_5_rating': 0,
            'chair_6_name': "",
            'chair_6_comment': "",
            'chair_6_rating': 0,
            'chair_7_name': "",
            'chair_7_comment': "",
            'chair_7_rating': 0,
            'chair_8_name': "",
            'chair_8_comment': "",
            'chair_8_rating': 0,
            'chair_9_name': "",
            'chair_9_comment': "",
            'chair_9_rating': 0,
            'chair_10_name': "",
            'chair_10_comment': "",
            'chair_10_rating': 0
        }

        self.params3 = {
            'comment': "Amazing",
            'rating': 9,
            'chair_1_name': "KT Lee",
            'chair_1_comment': "Best Chair 5evr",
            'chair_1_rating': 9,
            'chair_2_name': "Gent Tumberg",
            'chair_2_comment': "He was the jummy one",
            'chair_2_rating': 5,
            'chair_3_name': "Sita McLiar",
            'chair_3_comment': "",
            'chair_3_rating': 5,
            'chair_4_name': "The Spirit of BMUN",
            'chair_4_comment': "The Spirit of BMUN is ever strong",
            'chair_4_rating': 3,
            'chair_5_name': "Annalise!!!!",
            'chair_5_comment': "She's the best!!!!",
            'chair_5_rating': 9,
            'chair_6_name': "",
            'chair_6_comment': "",
            'chair_6_rating': 0,
            'chair_7_name': "",
            'chair_7_comment': "",
            'chair_7_rating': 0,
            'chair_8_name': "",
            'chair_8_comment': "",
            'chair_8_rating': 0,
            'chair_9_name': "",
            'chair_9_comment': "",
            'chair_9_rating': 0,
            'chair_10_name': "",
            'chair_10_comment': "",
            'chair_10_rating': 0
        }

        self.feedback_1 = models.new_committee_feedback(
            committee=self.committee_1,
            comment=self.params1['comment'],
            rating=self.params1['rating'],
            chair_1_name=self.params1['chair_1_name'],
            chair_1_comment=self.params1['chair_1_comment'],
            chair_1_rating=self.params1['chair_1_rating'],
            chair_2_name=self.params1['chair_2_name'],
            chair_2_comment=self.params1['chair_2_comment'],
            chair_2_rating=self.params1['chair_2_rating'],
            chair_3_name=self.params1['chair_3_name'],
            chair_3_comment=self.params1['chair_3_comment'],
            chair_3_rating=self.params1['chair_3_rating'],
            chair_4_name=self.params1['chair_4_name'],
            chair_4_comment=self.params1['chair_4_comment'],
            chair_4_rating=self.params1['chair_4_rating'],
            chair_5_name=self.params1['chair_5_name'],
            chair_5_comment=self.params1['chair_5_comment'],
            chair_5_rating=self.params1['chair_5_rating'],
            chair_6_name=self.params1['chair_6_name'],
            chair_6_comment=self.params1['chair_6_comment'],
            chair_6_rating=self.params1['chair_6_rating'],
            chair_7_name=self.params1['chair_7_name'],
            chair_7_comment=self.params1['chair_7_comment'],
            chair_7_rating=self.params1['chair_7_rating'],
            chair_8_name=self.params1['chair_8_name'],
            chair_8_comment=self.params1['chair_8_comment'],
            chair_8_rating=self.params1['chair_8_rating'],
            chair_9_name=self.params1['chair_9_name'],
            chair_9_comment=self.params1['chair_9_comment'],
            chair_9_rating=self.params1['chair_9_rating'],
            chair_10_name=self.params1['chair_10_name'],
            chair_10_comment=self.params1['chair_10_comment'],
            chair_10_rating=self.params1['chair_10_rating'])
        self.feedback_2 = models.new_committee_feedback(
            committee=self.committee_1,
            comment=self.params2['comment'],
            rating=self.params2['rating'],
            chair_1_name=self.params2['chair_1_name'],
            chair_1_comment=self.params2['chair_1_comment'],
            chair_1_rating=self.params2['chair_1_rating'],
            chair_2_name=self.params2['chair_2_name'],
            chair_2_comment=self.params2['chair_2_comment'],
            chair_2_rating=self.params2['chair_2_rating'],
            chair_3_name=self.params2['chair_3_name'],
            chair_3_comment=self.params2['chair_3_comment'],
            chair_3_rating=self.params2['chair_3_rating'],
            chair_4_name=self.params2['chair_4_name'],
            chair_4_comment=self.params2['chair_4_comment'],
            chair_4_rating=self.params2['chair_4_rating'],
            chair_5_name=self.params2['chair_5_name'],
            chair_5_comment=self.params2['chair_5_comment'],
            chair_5_rating=self.params2['chair_5_rating'],
            chair_6_name=self.params2['chair_6_name'],
            chair_6_comment=self.params2['chair_6_comment'],
            chair_6_rating=self.params2['chair_6_rating'],
            chair_7_name=self.params2['chair_7_name'],
            chair_7_comment=self.params2['chair_7_comment'],
            chair_7_rating=self.params2['chair_7_rating'],
            chair_8_name=self.params2['chair_8_name'],
            chair_8_comment=self.params2['chair_8_comment'],
            chair_8_rating=self.params2['chair_8_rating'],
            chair_9_name=self.params2['chair_9_name'],
            chair_9_comment=self.params2['chair_9_comment'],
            chair_9_rating=self.params2['chair_9_rating'],
            chair_10_name=self.params2['chair_10_name'],
            chair_10_comment=self.params2['chair_10_comment'],
            chair_10_rating=self.params2['chair_10_rating'])
        self.feedback_3 = models.new_committee_feedback(
            committee=self.committee_2,
            comment=self.params3['comment'],
            rating=self.params3['rating'],
            chair_1_name=self.params3['chair_1_name'],
            chair_1_comment=self.params3['chair_1_comment'],
            chair_1_rating=self.params3['chair_1_rating'],
            chair_2_name=self.params3['chair_2_name'],
            chair_2_comment=self.params3['chair_2_comment'],
            chair_2_rating=self.params3['chair_2_rating'],
            chair_3_name=self.params3['chair_3_name'],
            chair_3_comment=self.params3['chair_3_comment'],
            chair_3_rating=self.params3['chair_3_rating'],
            chair_4_name=self.params3['chair_4_name'],
            chair_4_comment=self.params3['chair_4_comment'],
            chair_4_rating=self.params3['chair_4_rating'],
            chair_5_name=self.params3['chair_5_name'],
            chair_5_comment=self.params3['chair_5_comment'],
            chair_5_rating=self.params3['chair_5_rating'],
            chair_6_name=self.params3['chair_6_name'],
            chair_6_comment=self.params3['chair_6_comment'],
            chair_6_rating=self.params3['chair_6_rating'],
            chair_7_name=self.params3['chair_7_name'],
            chair_7_comment=self.params3['chair_7_comment'],
            chair_7_rating=self.params3['chair_7_rating'],
            chair_8_name=self.params3['chair_8_name'],
            chair_8_comment=self.params3['chair_8_comment'],
            chair_8_rating=self.params3['chair_8_rating'],
            chair_9_name=self.params3['chair_9_name'],
            chair_9_comment=self.params3['chair_9_comment'],
            chair_9_rating=self.params3['chair_9_rating'],
            chair_10_name=self.params3['chair_10_name'],
            chair_10_comment=self.params3['chair_10_comment'],
            chair_10_rating=self.params3['chair_10_rating'])
        self.assignment_1 = models.new_assignment(committee=self.committee_1)

    def test_anonymous_user(self):
        '''Anonymous users cannot retrieve feedback'''
        response = self.get_response()
        self.assertNotAuthenticated(response)

    def test_delegate(self):
        '''Delegate cannot retrieve committee feedback'''
        self.user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE,
            assignment=self.assignment_1, )
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(
            params={'committee_id': self.committee_1.id})
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Chair can retrieve feedback of chair's committee'''
        self.user = models.new_user(
            username='chair',
            password='chair',
            user_type=User.TYPE_CHAIR,
            committee_id=self.committee_1.id, )
        self.client.login(username='chair', password='chair')
        response_1 = self.get_response(
            params={'committee_id': self.committee_1.id})
        self.assertEqual(response_1.data, [
            {
                'id': self.feedback_1.id,
                'committee': self.committee_1.id,
                'comment': self.feedback_1.comment,
                'rating': self.feedback_1.rating,
                'chair_1_name': self.feedback_1.chair_1_name,
                'chair_1_comment': self.feedback_1.chair_1_comment,
                'chair_1_rating': self.feedback_1.chair_1_rating,
                'chair_2_name': self.feedback_1.chair_2_name,
                'chair_2_comment': self.feedback_1.chair_2_comment,
                'chair_2_rating': self.feedback_1.chair_2_rating,
                'chair_3_name': self.feedback_1.chair_3_name,
                'chair_3_comment': self.feedback_1.chair_3_comment,
                'chair_3_rating': self.feedback_1.chair_3_rating,
                'chair_4_name': self.feedback_1.chair_4_name,
                'chair_4_comment': self.feedback_1.chair_4_comment,
                'chair_4_rating': self.feedback_1.chair_4_rating,
                'chair_5_name': self.feedback_1.chair_5_name,
                'chair_5_comment': self.feedback_1.chair_5_comment,
                'chair_5_rating': self.feedback_1.chair_5_rating,
                'chair_6_name': self.feedback_1.chair_6_name,
                'chair_6_comment': self.feedback_1.chair_6_comment,
                'chair_6_rating': self.feedback_1.chair_6_rating,
                'chair_7_name': self.feedback_1.chair_7_name,
                'chair_7_comment': self.feedback_1.chair_7_comment,
                'chair_7_rating': self.feedback_1.chair_7_rating,
                'chair_8_name': self.feedback_1.chair_8_name,
                'chair_8_comment': self.feedback_1.chair_8_comment,
                'chair_8_rating': self.feedback_1.chair_8_rating,
                'chair_9_name': self.feedback_1.chair_9_name,
                'chair_9_comment': self.feedback_1.chair_9_comment,
                'chair_9_rating': self.feedback_1.chair_9_rating,
                'chair_10_name': self.feedback_1.chair_10_name,
                'chair_10_comment': self.feedback_1.chair_10_comment,
                'chair_10_rating': self.feedback_1.chair_10_rating
            }, {
                'id': self.feedback_2.id,
                'committee': self.committee_1.id,
                'comment': self.feedback_2.comment,
                'rating': self.feedback_2.rating,
                'chair_1_name': self.feedback_2.chair_1_name,
                'chair_1_comment': self.feedback_2.chair_1_comment,
                'chair_1_rating': self.feedback_2.chair_1_rating,
                'chair_2_name': self.feedback_2.chair_2_name,
                'chair_2_comment': self.feedback_2.chair_2_comment,
                'chair_2_rating': self.feedback_2.chair_2_rating,
                'chair_3_name': self.feedback_2.chair_3_name,
                'chair_3_comment': self.feedback_2.chair_3_comment,
                'chair_3_rating': self.feedback_2.chair_3_rating,
                'chair_4_name': self.feedback_2.chair_4_name,
                'chair_4_comment': self.feedback_2.chair_4_comment,
                'chair_4_rating': self.feedback_2.chair_4_rating,
                'chair_5_name': self.feedback_2.chair_5_name,
                'chair_5_comment': self.feedback_2.chair_5_comment,
                'chair_5_rating': self.feedback_2.chair_5_rating,
                'chair_6_name': self.feedback_2.chair_6_name,
                'chair_6_comment': self.feedback_2.chair_6_comment,
                'chair_6_rating': self.feedback_2.chair_6_rating,
                'chair_7_name': self.feedback_2.chair_7_name,
                'chair_7_comment': self.feedback_2.chair_7_comment,
                'chair_7_rating': self.feedback_2.chair_7_rating,
                'chair_8_name': self.feedback_2.chair_8_name,
                'chair_8_comment': self.feedback_2.chair_8_comment,
                'chair_8_rating': self.feedback_2.chair_8_rating,
                'chair_9_name': self.feedback_2.chair_9_name,
                'chair_9_comment': self.feedback_2.chair_9_comment,
                'chair_9_rating': self.feedback_2.chair_9_rating,
                'chair_10_name': self.feedback_2.chair_10_name,
                'chair_10_comment': self.feedback_2.chair_10_comment,
                'chair_10_rating': self.feedback_2.chair_10_rating
            }
        ])
        response_2 = self.get_response(
            params={'committee': self.committee_2.id})
        self.assertPermissionDenied(response_2)

    def test_advisor(self):
        '''Advisor cannot retrive committee feedback'''
        self.user = models.new_user(
            username='advisor',
            password='advisor',
            user_type=User.TYPE_ADVISOR, )
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(
            params={'committee_id': self.committee_1.id})
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''Superuser can retrieve all feedback'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response_1 = self.get_response(
            params={'committee_id': self.committee_1.id})
        self.assertEqual(response_1.data, [
            {
                'id': self.feedback_1.id,
                'committee': self.committee_1.id,
                'comment': self.feedback_1.comment,
                'rating': self.feedback_1.rating,
                'chair_1_name': self.feedback_1.chair_1_name,
                'chair_1_comment': self.feedback_1.chair_1_comment,
                'chair_1_rating': self.feedback_1.chair_1_rating,
                'chair_2_name': self.feedback_1.chair_2_name,
                'chair_2_comment': self.feedback_1.chair_2_comment,
                'chair_2_rating': self.feedback_1.chair_2_rating,
                'chair_3_name': self.feedback_1.chair_3_name,
                'chair_3_comment': self.feedback_1.chair_3_comment,
                'chair_3_rating': self.feedback_1.chair_3_rating,
                'chair_4_name': self.feedback_1.chair_4_name,
                'chair_4_comment': self.feedback_1.chair_4_comment,
                'chair_4_rating': self.feedback_1.chair_4_rating,
                'chair_5_name': self.feedback_1.chair_5_name,
                'chair_5_comment': self.feedback_1.chair_5_comment,
                'chair_5_rating': self.feedback_1.chair_5_rating,
                'chair_6_name': self.feedback_1.chair_6_name,
                'chair_6_comment': self.feedback_1.chair_6_comment,
                'chair_6_rating': self.feedback_1.chair_6_rating,
                'chair_7_name': self.feedback_1.chair_7_name,
                'chair_7_comment': self.feedback_1.chair_7_comment,
                'chair_7_rating': self.feedback_1.chair_7_rating,
                'chair_8_name': self.feedback_1.chair_8_name,
                'chair_8_comment': self.feedback_1.chair_8_comment,
                'chair_8_rating': self.feedback_1.chair_8_rating,
                'chair_9_name': self.feedback_1.chair_9_name,
                'chair_9_comment': self.feedback_1.chair_9_comment,
                'chair_9_rating': self.feedback_1.chair_9_rating,
                'chair_10_name': self.feedback_1.chair_10_name,
                'chair_10_comment': self.feedback_1.chair_10_comment,
                'chair_10_rating': self.feedback_1.chair_10_rating
            }, {
                'id': self.feedback_2.id,
                'committee': self.committee_1.id,
                'comment': self.feedback_2.comment,
                'rating': self.feedback_2.rating,
                'chair_1_name': self.feedback_2.chair_1_name,
                'chair_1_comment': self.feedback_2.chair_1_comment,
                'chair_1_rating': self.feedback_2.chair_1_rating,
                'chair_2_name': self.feedback_2.chair_2_name,
                'chair_2_comment': self.feedback_2.chair_2_comment,
                'chair_2_rating': self.feedback_2.chair_2_rating,
                'chair_3_name': self.feedback_2.chair_3_name,
                'chair_3_comment': self.feedback_2.chair_3_comment,
                'chair_3_rating': self.feedback_2.chair_3_rating,
                'chair_4_name': self.feedback_2.chair_4_name,
                'chair_4_comment': self.feedback_2.chair_4_comment,
                'chair_4_rating': self.feedback_2.chair_4_rating,
                'chair_5_name': self.feedback_2.chair_5_name,
                'chair_5_comment': self.feedback_2.chair_5_comment,
                'chair_5_rating': self.feedback_2.chair_5_rating,
                'chair_6_name': self.feedback_2.chair_6_name,
                'chair_6_comment': self.feedback_2.chair_6_comment,
                'chair_6_rating': self.feedback_2.chair_6_rating,
                'chair_7_name': self.feedback_2.chair_7_name,
                'chair_7_comment': self.feedback_2.chair_7_comment,
                'chair_7_rating': self.feedback_2.chair_7_rating,
                'chair_8_name': self.feedback_2.chair_8_name,
                'chair_8_comment': self.feedback_2.chair_8_comment,
                'chair_8_rating': self.feedback_2.chair_8_rating,
                'chair_9_name': self.feedback_2.chair_9_name,
                'chair_9_comment': self.feedback_2.chair_9_comment,
                'chair_9_rating': self.feedback_2.chair_9_rating,
                'chair_10_name': self.feedback_2.chair_10_name,
                'chair_10_comment': self.feedback_2.chair_10_comment,
                'chair_10_rating': self.feedback_2.chair_10_rating
            }
        ])
        response_2 = self.get_response(
            params={'committee_id': self.committee_2.id})
        self.assertEqual(response_2.data, [{
            'id': self.feedback_3.id,
            'committee': self.committee_2.id,
            'comment': self.feedback_3.comment,
            'rating': self.feedback_3.rating,
            'chair_1_name': self.feedback_3.chair_1_name,
            'chair_1_comment': self.feedback_3.chair_1_comment,
            'chair_1_rating': self.feedback_3.chair_1_rating,
            'chair_2_name': self.feedback_3.chair_2_name,
            'chair_2_comment': self.feedback_3.chair_2_comment,
            'chair_2_rating': self.feedback_3.chair_2_rating,
            'chair_3_name': self.feedback_3.chair_3_name,
            'chair_3_comment': self.feedback_3.chair_3_comment,
            'chair_3_rating': self.feedback_3.chair_3_rating,
            'chair_4_name': self.feedback_3.chair_4_name,
            'chair_4_comment': self.feedback_3.chair_4_comment,
            'chair_4_rating': self.feedback_3.chair_4_rating,
            'chair_5_name': self.feedback_3.chair_5_name,
            'chair_5_comment': self.feedback_3.chair_5_comment,
            'chair_5_rating': self.feedback_3.chair_5_rating,
            'chair_6_name': self.feedback_3.chair_6_name,
            'chair_6_comment': self.feedback_3.chair_6_comment,
            'chair_6_rating': self.feedback_3.chair_6_rating,
            'chair_7_name': self.feedback_3.chair_7_name,
            'chair_7_comment': self.feedback_3.chair_7_comment,
            'chair_7_rating': self.feedback_3.chair_7_rating,
            'chair_8_name': self.feedback_3.chair_8_name,
            'chair_8_comment': self.feedback_3.chair_8_comment,
            'chair_8_rating': self.feedback_3.chair_8_rating,
            'chair_9_name': self.feedback_3.chair_9_name,
            'chair_9_comment': self.feedback_3.chair_9_comment,
            'chair_9_rating': self.feedback_3.chair_9_rating,
            'chair_10_name': self.feedback_3.chair_10_name,
            'chair_10_comment': self.feedback_3.chair_10_comment,
            'chair_10_rating': self.feedback_3.chair_10_rating
        }])
