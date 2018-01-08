# copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.exceptions import ValidationError

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models
import random


class CommitteeFeedbackDetailCreateTestCase(tests.CreateSingleAPITestCase):
    url_name = 'api:committee_feedback_detail'

    def setUp(self):
        self.committee_1 = models.new_committee(name='CYBER')
        self.committee_2 = models.new_committee(name='UNPBC')
        self.assignment = models.new_assignment(committee=self.committee_1)
        self.delegate = models.new_delegate(assignment=self.assignment)
        self.params = {
            'comment': "I never got called on ever. SAD!",
            'committee': self.committee_1.id
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
            delegate=self.delegate,
            assignment=self.assignment)
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
        })


class CommitteeFeedbackDetailGetTestCase(tests.RetrieveAPITestCase):
    url_name = 'api:committee_feedback_detail'

    def setUp(self):
        self.committee_1 = models.new_committee(name='UNSC')
        self.feedback_1 = models.new_committee_feedback(
            committee=self.committee_1, comment='Good')
        self.committee_2 = models.new_committee(name='HSC')
        self.feedback_2 = models.new_committee_feedback(
            committee=self.committee_2, comment='Not Good')
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
        self.assertEqual(response_1.data, {'committee': self.committee_1.id,
                                           'comment': self.feedback_1.comment})
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
        self.assertEqual(response_1.data, {'committee': self.committee_1.id,
                                           'comment': self.feedback_1.comment})
        response_2 = self.get_response(self.feedback_2.id)
        response_2.data.pop('id')
        self.assertEqual(response_2.data, {'committee': self.committee_2.id,
                                           'comment': self.feedback_2.comment})


class CommitteeFeedbackListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:committee_feedback_list'

    def setUp(self):
        self.committee_1 = models.new_committee(name='DISC')
        self.committee_2 = models.new_committee(name='SOCHUM')
        self.feedback_1 = models.new_committee_feedback(
            committee=self.committee_1, comment='Good')
        self.feedback_2 = models.new_committee_feedback(
            committee=self.committee_1, comment="Not so good")
        self.feedback_3 = models.new_committee_feedback(
            committee=self.committee_2, comment="Awful")
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
            {'id': self.feedback_1.id,
             'committee': self.committee_1.id,
             'comment': self.feedback_1.comment},
            {'id': self.feedback_2.id,
             'committee': self.committee_1.id,
             'comment': self.feedback_2.comment}
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
            {'id': self.feedback_1.id,
             'committee': self.committee_1.id,
             'comment': self.feedback_1.comment},
            {'id': self.feedback_2.id,
             'committee': self.committee_1.id,
             'comment': self.feedback_2.comment}
        ])
        response_2 = self.get_response(
            params={'committee_id': self.committee_2.id})
        self.assertEqual(response_2.data, [
            {'id': self.feedback_3.id,
             'committee': self.committee_2.id,
             'comment': self.feedback_3.comment}
        ])
