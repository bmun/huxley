# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.exceptions import ValidationError

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models


class PositionPaperDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:position_paper_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_position_paper()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        a = models.new_assignment(paper_id=self.object.id)
        user = models.new_user(school=a.registration.school.id)
        self.as_user(user).do_test()

    def test_chair(self):
        a = models.new_assignment(paper_id=self.object.id)
        chair = models.new_user(
            user_type=User.TYPE_CHAIR,
            committee=a.committee)
        self.as_user(chair).do_test()

    def test_other_chair(self):
        a = models.new_assignment()
        chair = models.new_user(
            user_type=User.TYPE_CHAIR,
            committee=a.committee)
        self.as_user(chair).do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_delegate(self):
        a = models.new_assignment(paper_id=self.object.id)

        delegate_user = models.new_user(user_type=User.TYPE_DELEGATE)
        self.as_user(delegate_user).do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

        delegate = models.new_delegate(assignment=a, school=a.registration.school, user=delegate_user)
        self.as_user(delegate_user).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()


class PositionPaperPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:position_paper_detail'
    params = {
        'score_1': 5,
        'score_2': 5,
    }

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.chair = models.new_user(
            username='chair', password='chair', user_type=User.TYPE_CHAIR)
        self.delegate_user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.delegate_user_2 = models.new_user(
            username='delegate_2',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.school = models.new_school(user=self.advisor)
        self.registration = models.new_registration(school=self.school)
        self.committee = models.new_committee(user=self.chair)
        self.paper = models.new_position_paper()
        self.assignment = models.new_assignment(
            registration=self.registration, committee=self.committee, paper=self.paper)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            assignment=self.assignment,
            school=self.school)
        self.params['assignment'] = self.assignment.id

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update position papers.'''
        response = self.get_response(self.delegate.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors shouldn't be able to update position papers.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied()

    def test_chair(self):
        '''It should return correct data.'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "score_1": self.params['score_1'],
            "score_2": self.params['score_2'],
            "score_3": self.paper.score_3,
            "score_4": self.paper.score_4,
            "score_5": self.paper.score_5,
            "graded": self.paper.graded,
            "file": self.paper.file
        })

    def test_delegate(self):
        '''It should return correct data.'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "score_1": self.params['score_1'],
            "score_2": self.params['score_2'],
            "score_3": self.paper.score_3,
            "score_4": self.paper.score_4,
            "score_5": self.paper.score_5,
            "graded": self.paper.graded,
            "file": self.paper.file
        })

    def test_other_delegate(self):
        '''A delegate shouldn't be able to update a position paper they do not possess.'''
        self.client.login(username='delegate_2', password='delegate')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied()

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "score_1": self.params['score_1'],
            "score_2": self.params['score_2'],
            "score_3": self.paper.score_3,
            "score_4": self.paper.score_4,
            "score_5": self.paper.score_5,
            "graded": self.paper.graded,
            "file": self.paper.file
        })


class PositionPaperDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:delegate_detail'
    params = {
        'score_1': 5,
        'score_2': 5,
    }

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.chair = models.new_user(
            username='chair', password='chair', user_type=User.TYPE_CHAIR)
        self.delegate_user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.delegate_user_2 = models.new_user(
            username='delegate_2',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.school = models.new_school(user=self.advisor)
        self.registration = models.new_registration(school=self.school)
        self.committee = models.new_committee(user=self.chair)
        self.paper = models.new_position_paper()
        self.assignment = models.new_assignment(
            registration=self.registration, committee=self.committee, paper=self.paper)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            assignment=self.assignment,
            school=self.school)
        self.params['assignment'] = self.assignment.id

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update position papers.'''
        response = self.get_response(self.delegate.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors shouldn't be able to update position papers.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied()

    def test_chair(self):
        '''It should return correct data.'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "score_1": self.params['score_1'],
            "score_2": self.params['score_2'],
            "score_3": self.paper.score_3,
            "score_4": self.paper.score_4,
            "score_5": self.paper.score_5,
            "graded": self.paper.graded,
            "file": self.paper.file
        })

    def test_delegate(self):
        '''It should return correct data.'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "score_1": self.params['score_1'],
            "score_2": self.params['score_2'],
            "score_3": self.paper.score_3,
            "score_4": self.paper.score_4,
            "score_5": self.paper.score_5,
            "graded": self.paper.graded,
            "file": self.paper.file
        })

    def test_other_delegate(self):
        '''A delegate shouldn't be able to update a position paper they do not possess.'''
        self.client.login(username='delegate_2', password='delegate')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied()

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "score_1": self.params['score_1'],
            "score_2": self.params['score_2'],
            "score_3": self.paper.score_3,
            "score_4": self.paper.score_4,
            "score_5": self.paper.score_5,
            "graded": self.paper.graded,
            "file": self.paper.file
        })
