# copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.exceptions import ValidationError
from collections import OrderedDict

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models
from huxley.core.constants import SpeechTypes
import random

class SpeechListGetTestCase(tests.ListAPITestCase):
    '''Tests to see that anyone can retrieve secretariat member list information'''
    url_name = "api:speech_list"

    def setUp(self):
        self.assi1 = models.new_assignment()
        self.assi2 = models.new_assignment()
        self.sp1 = models.new_speech(assignment=self.assi1)
        self.sp2 = models.new_speech(assignment=self.assi1, speechtype=SpeechTypes.QUESTION)

    def test_anonymous_user(self):
        '''Tests anonymous user can not get speech list'''
        response = self.get_response()
        self.assertNotAuthenticated(response)

    def test_delegate(self):
        '''Delegate cannot retrieve speeches'''
        self.user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE,
            assignment=self.assi1, )
        self.client.login(username='delegate', password='delegate')
        response = self.get_response()
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Tests chair can get speeches'''
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
                'assignment': OrderedDict(
                [('id', self.assi1.paper.id),
                 ('file', self.assi1.paper.file),
                 ('graded_file', self.assi1.paper.graded_file),
                 ('graded', self.assi1.paper.graded),
                 ('score_1', self.assi1.paper.score_1),
                 ('score_2', self.assi1.paper.score_2),
                 ('score_3', self.assi1.paper.score_3),
                 ('score_4', self.assi1.paper.score_4),
                 ('score_5', self.assi1.paper.score_5),
                 ('score_t2_1', self.assi1.paper.score_t2_1),
                 ('score_t2_2', self.assi1.paper.score_t2_2),
                 ('score_t2_3', self.assi1.paper.score_t2_3),
                 ('score_t2_4', self.assi1.paper.score_t2_4),
                 ('score_t2_5', self.assi1.paper.score_t2_5),
                 ("submission_date", self.assi1.paper.submission_date)]),
                'speechtype': SpeechTypes.SPEAKER,
            }, {
                'assignment': OrderedDict(
                [('id', self.assi2.paper.id),
                 ('file', self.assi2.paper.file),
                 ('graded_file', self.assi2.paper.graded_file),
                 ('graded', self.assi2.paper.graded),
                 ('score_1', self.assi2.paper.score_1),
                 ('score_2', self.assi2.paper.score_2),
                 ('score_3', self.assi2.paper.score_3),
                 ('score_4', self.assi2.paper.score_4),
                 ('score_5', self.assi2.paper.score_5),
                 ('score_t2_1', self.assi2.paper.score_t2_1),
                 ('score_t2_2', self.assi2.paper.score_t2_2),
                 ('score_t2_3', self.assi2.paper.score_t2_3),
                 ('score_t2_4', self.assi2.paper.score_t2_4),
                 ('score_t2_5', self.assi2.paper.score_t2_5),
                 ("submission_date", self.assi2.paper.submission_date)]),
                'speechtype': SpeechTypes.QUESTION,
            }
        ])

    def test_advisor(self):
        '''Tests advisor can not get speeches'''
        self.user = models.new_user(
            username='advisor',
            password='advisor',
            user_type=User.TYPE_ADVISOR, )
        self.client.login(username='advisor', password='advisor')
        response = self.get_response()
        self.assertPermissionDenied(response)


    def test_superuser(self):
        '''Tests superuser can get secretariat information'''
        models.new_superuser(username='user', password='user')
        self.client.login(username='user', password='user')
        response = self.get_response()
        self.assertEqual(response.data, [
            {
                'assignment': OrderedDict(
                [('id', self.assi1.paper.id),
                 ('file', self.assi1.paper.file),
                 ('graded_file', self.assi1.paper.graded_file),
                 ('graded', self.assi1.paper.graded),
                 ('score_1', self.assi1.paper.score_1),
                 ('score_2', self.assi1.paper.score_2),
                 ('score_3', self.assi1.paper.score_3),
                 ('score_4', self.assi1.paper.score_4),
                 ('score_5', self.assi1.paper.score_5),
                 ('score_t2_1', self.assi1.paper.score_t2_1),
                 ('score_t2_2', self.assi1.paper.score_t2_2),
                 ('score_t2_3', self.assi1.paper.score_t2_3),
                 ('score_t2_4', self.assi1.paper.score_t2_4),
                 ('score_t2_5', self.assi1.paper.score_t2_5),
                 ("submission_date", self.assi1.paper.submission_date)]),
                'speechtype': SpeechTypes.SPEAKER,
            }, {
                'assignment': OrderedDict(
                [('id', self.assi2.paper.id),
                 ('file', self.assi2.paper.file),
                 ('graded_file', self.assi2.paper.graded_file),
                 ('graded', self.assi2.paper.graded),
                 ('score_1', self.assi2.paper.score_1),
                 ('score_2', self.assi2.paper.score_2),
                 ('score_3', self.assi2.paper.score_3),
                 ('score_4', self.assi2.paper.score_4),
                 ('score_5', self.assi2.paper.score_5),
                 ('score_t2_1', self.assi2.paper.score_t2_1),
                 ('score_t2_2', self.assi2.paper.score_t2_2),
                 ('score_t2_3', self.assi2.paper.score_t2_3),
                 ('score_t2_4', self.assi2.paper.score_t2_4),
                 ('score_t2_5', self.assi2.paper.score_t2_5),
                 ("submission_date", self.assi2.paper.submission_date)]),
                'speechtype': SpeechTypes.QUESTION,
            }
        ])