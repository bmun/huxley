# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import os

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
        user = models.new_user()
        school = models.new_school(user=user)
        registration = models.new_registration(school=school)
        a = models.new_assignment(paper=self.object, registration=registration)
        self.as_user(user).do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_chair(self):
        a = models.new_assignment(paper=self.object)
        chair = models.new_user(
            user_type=User.TYPE_CHAIR, committee=a.committee)
        self.as_user(chair).do_test()

    def test_other_chair(self):
        a = models.new_assignment()
        chair = models.new_user(
            user_type=User.TYPE_CHAIR, committee=a.committee)
        self.as_user(chair).do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_delegate(self):
        a = models.new_assignment(paper=self.object)

        delegate_user = models.new_user(user_type=User.TYPE_DELEGATE)
        self.as_user(delegate_user).do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

        delegate = models.new_delegate(
            assignment=a, school=a.registration.school, user=delegate_user)
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
            registration=self.registration,
            committee=self.committee,
            paper=self.paper)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            assignment=self.assignment,
            school=self.school)

    def get_response(self, object_id=None, params=None):
        if self.method is None:
            raise NotImplementedError('Must define method class member.')

        params = params or self.params

        request = getattr(self.client, self.method)
        url = self.get_url(object_id)
        return request(url, params)

    def test_anonymous_user(self):
        '''Unauthenticated users should be unable to update position papers.'''
        response = self.get_response(self.delegate.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors should be unable to update position papers.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied(response)

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
            "score_t2_1": self.paper.score_t2_1,
            "score_t2_2": self.paper.score_t2_2,
            "score_t2_3": self.paper.score_t2_3,
            "score_t2_4": self.paper.score_t2_4,
            "score_t2_5": self.paper.score_t2_5,
            "graded": self.paper.graded,
            "graded_file": self.paper.graded_file,
            "file": self.paper.file,
            "submission_date": self.paper.submission_date
        })

    def test_delegate_scores(self):
        '''Delegates should be unable to update scores.'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_delegate_file(self):
        '''Delegates should be able to update the file.'''
        if os.path.isfile('test_position_paper.doc'):
            os.remove('test_position_paper.doc')
        if os.path.isfile('position_papers/test_position_paper.doc'):
            os.remove('position_papers/test_position_paper.doc')
        self.client.login(username='delegate', password='delegate')
        with open('test_position_paper.doc', 'a+') as f:
            f.write('This is a test line.')

        f = open('test_position_paper.doc', 'r')
        response = self.get_response(self.paper.id, params={"file": f})
        f.close()

        f = open('test_position_paper.doc', 'r')
        new_file = response.data.pop("file", None)
        self.assertTrue(
            new_file != None and new_file ==
            "http://testserver/api/papers/position_papers/test_position_paper.doc")
        new_f = open('position_papers/test_position_paper.doc', 'r')
        self.assertEqual(f.read(), new_f.read())
        f.close()
        new_f.close()
        os.remove('test_position_paper.doc')
        os.remove('position_papers/test_position_paper.doc')

    def test_other_delegate(self):
        '''A delegate should be unable to update a position paper they do not possess.'''
        self.client.login(username='delegate_2', password='delegate')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied(response)

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
            "score_t2_1": self.paper.score_t2_1,
            "score_t2_2": self.paper.score_t2_2,
            "score_t2_3": self.paper.score_t2_3,
            "score_t2_4": self.paper.score_t2_4,
            "score_t2_5": self.paper.score_t2_5,
            "graded": self.paper.graded,
            "graded_file": self.paper.graded_file,
            "file": self.paper.file,
            "submission_date": self.paper.submission_date
        })


class PositionPaperDetailPatchTestCase(tests.PartialUpdateAPITestCase):
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
            registration=self.registration,
            committee=self.committee,
            paper=self.paper)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            assignment=self.assignment,
            school=self.school)

    def get_response(self, object_id=None, params=None):
        if self.method is None:
            raise NotImplementedError('Must define method class member.')

        params = params or self.params

        request = getattr(self.client, self.method)
        url = self.get_url(object_id)
        return request(url, params)

    def test_anonymous_user(self):
        '''Unauthenticated users should be unable able to update position papers.'''
        response = self.get_response(self.paper.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors should be unable to update position papers.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied(response)

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
            "score_t2_1": self.paper.score_t2_1,
            "score_t2_2": self.paper.score_t2_2,
            "score_t2_3": self.paper.score_t2_3,
            "score_t2_4": self.paper.score_t2_4,
            "score_t2_5": self.paper.score_t2_5,
            "graded": self.paper.graded,
            "graded_file": self.paper.graded_file,
            "file": self.paper.file,
            "submission_date": self.paper.submission_date
        })

    def test_delegate_scores(self):
        '''Delegates should be unable to update scores.'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_delegate_file(self):
        '''Delegates should be able to update the file.'''
        if os.path.isfile('test_position_paper.doc'):
            os.remove('test_position_paper.doc')
        if os.path.isfile('position_papers/test_position_paper.doc'):
            os.remove('position_papers/test_position_paper.doc')
        self.client.login(username='delegate', password='delegate')
        with open('test_position_paper.doc', 'a+') as f:
            f.write('This is a test line.')

        f = open('test_position_paper.doc', 'r')
        response = self.get_response(self.paper.id, params={"file": f})
        f.close()

        f = open('test_position_paper.doc', 'r')
        new_file = response.data.pop("file", None)
        self.assertTrue(
            new_file != None and new_file ==
            "http://testserver/api/papers/position_papers/test_position_paper.doc")
        new_f = open('position_papers/test_position_paper.doc', 'r')
        self.assertEqual(f.read(), new_f.read())
        f.close()
        new_f.close()
        os.remove('test_position_paper.doc')
        os.remove('position_papers/test_position_paper.doc')

    def test_other_delegate(self):
        '''A delegate should be unable to update a position paper they do not possess.'''
        self.client.login(username='delegate_2', password='delegate')
        response = self.get_response(self.paper.id, params=self.params)
        self.assertPermissionDenied(response)

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
            "score_t2_1": self.paper.score_t2_1,
            "score_t2_2": self.paper.score_t2_2,
            "score_t2_3": self.paper.score_t2_3,
            "score_t2_4": self.paper.score_t2_4,
            "score_t2_5": self.paper.score_t2_5,
            "graded": self.paper.graded,
            "graded_file": self.paper.graded_file,
            "file": self.paper.file,
            "submission_date": self.paper.submission_date
        })
