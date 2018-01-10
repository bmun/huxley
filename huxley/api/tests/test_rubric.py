# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.exceptions import ValidationError

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models


class RubricDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:rubric_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_rubric()

    def test_anonymous_user(self):
        self.do_test()

    def test_advisor(self):
        user = models.new_user()
        self.as_user(user).do_test()

    def test_chair(self):
        chair1 = models.new_user(user_type=User.TYPE_CHAIR)
        self.as_user(chair1).do_test()
        c = models.new_committee(rubric_id=self.object.id)
        chair2 = models.new_user(
            user_type=User.TYPE_CHAIR,
            committee=c)
        self.as_user(chair2).do_test()

    def test_delegate(self):
        delegate_user = models.new_user(user_type=User.TYPE_DELEGATE)
        self.as_user(delegate_user).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()


class RubricPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:rubric_detail'
    params = {
        'grade_category_1': 'Overall Quality',
        'grade_value_1': 5,
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
        self.rubric = models.new_rubric()
        self.committee = models.new_committee(user=self.chair, rubric=self.rubric)
        self.paper = models.new_position_paper()
        self.assignment = models.new_assignment(
            registration=self.registration, committee=self.committee, paper=self.paper)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            assignment=self.assignment,
            school=self.school)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update rubrics.'''
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors shouldn't be able to update rubrics.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''It should return correct data.'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "grade_category_1": self.params['grade_category_1'],
            "grade_value_1": self.params['grade_value_1'],
            "grade_category_2": self.rubric.grade_category_2,
            "grade_value_2": self.rubric.grade_value_2,
            "grade_category_3": self.rubric.grade_category_3,
            "grade_value_3": self.rubric.grade_value_3,
            "grade_category_4": self.rubric.grade_category_4,
            "grade_value_4": self.rubric.grade_value_4,
            "grade_category_5": self.rubric.grade_category_5,
            "grade_value_5": self.rubric.grade_value_5,
        })

    def test_delegate(self):
        '''Delegates should be unable to update rubrics.'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertPermissionDenied(response)

        self.client.login(username='delegate_2', password='delegate')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "grade_category_1": self.params['grade_category_1'],
            "grade_value_1": self.params['grade_value_1'],
            "grade_category_2": self.rubric.grade_category_2,
            "grade_value_2": self.rubric.grade_value_2,
            "grade_category_3": self.rubric.grade_category_3,
            "grade_value_3": self.rubric.grade_value_3,
            "grade_category_4": self.rubric.grade_category_4,
            "grade_value_4": self.rubric.grade_value_4,
            "grade_category_5": self.rubric.grade_category_5,
            "grade_value_5": self.rubric.grade_value_5,
        })


class RubricDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:rubric_detail'
    params = {
        'grade_category_1': 'Overall Quality',
        'grade_value_1': 5,
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
        self.rubric = models.new_rubric()
        self.committee = models.new_committee(user=self.chair, rubric=self.rubric)
        self.paper = models.new_position_paper()
        self.assignment = models.new_assignment(
            registration=self.registration, committee=self.committee, paper=self.paper)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            assignment=self.assignment,
            school=self.school)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update rubrics.'''
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors shouldn't be able to update rubrics.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''It should return correct data.'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "grade_category_1": self.params['grade_category_1'],
            "grade_value_1": self.params['grade_value_1'],
            "grade_category_2": self.rubric.grade_category_2,
            "grade_value_2": self.rubric.grade_value_2,
            "grade_category_3": self.rubric.grade_category_3,
            "grade_value_3": self.rubric.grade_value_3,
            "grade_category_4": self.rubric.grade_category_4,
            "grade_value_4": self.rubric.grade_value_4,
            "grade_category_5": self.rubric.grade_category_5,
            "grade_value_5": self.rubric.grade_value_5,
        })

    def test_delegate(self):
        '''Delegates should be unable to update rubrics.'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertPermissionDenied(response)

        self.client.login(username='delegate_2', password='delegate')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.rubric.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.paper.id,
            "grade_category_1": self.params['grade_category_1'],
            "grade_value_1": self.params['grade_value_1'],
            "grade_category_2": self.rubric.grade_category_2,
            "grade_value_2": self.rubric.grade_value_2,
            "grade_category_3": self.rubric.grade_category_3,
            "grade_value_3": self.rubric.grade_value_3,
            "grade_category_4": self.rubric.grade_category_4,
            "grade_value_4": self.rubric.grade_value_4,
            "grade_category_5": self.rubric.grade_category_5,
            "grade_value_5": self.rubric.grade_value_5,
        })
