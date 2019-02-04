# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from collections import OrderedDict

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models


class AssignmentDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:assignment_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_assignment()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        self.as_user(self.object.registration.school.advisor).do_test()

    def test_chair(self):
        chair = models.new_user(user_type=User.TYPE_CHAIR)
        self.as_user(chair).do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_delegate(self):
        delegate_1 = models.new_user(user_type=User.TYPE_DELEGATE)
        self.as_user(delegate_1).do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

        assigned_delegate = models.new_delegate(assignment=self.object)
        delegate_2 = models.new_user(
            user_type=User.TYPE_DELEGATE, delegate=assigned_delegate)
        self.as_user(delegate_2).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()


class AssignmentDetailPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:assignment_detail'
    params = {'rejected': True}

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.school = models.new_school(user=self.advisor)
        self.registration = models.new_registration(school=self.school)
        self.chair = models.new_user(
            username='chair', password='chair', user_type=User.TYPE_CHAIR)
        self.committee = models.new_committee(user=self.chair)
        self.assignment = models.new_assignment(
            committee=self.committee, registration=self.registration)
        self.delegate_user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            school=self.school,
            assignment=self.assignment)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update assignments.'''
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It should return correct data.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.assignment.id,
            "committee": self.assignment.committee.id,
            "country": self.assignment.country.id,
            "registration": self.registration.id,
            "paper": OrderedDict(
                [('id', self.assignment.paper.id),
                 ('file', self.assignment.paper.file),
                 ('graded_file', self.assignment.paper.graded_file),
                 ('graded', self.assignment.paper.graded),
                 ('score_1', self.assignment.paper.score_1),
                 ('score_2', self.assignment.paper.score_2),
                 ('score_3', self.assignment.paper.score_3),
                 ('score_4', self.assignment.paper.score_4),
                 ('score_5', self.assignment.paper.score_5),
                 ('score_t2_1', self.assignment.paper.score_t2_1),
                 ('score_t2_2', self.assignment.paper.score_t2_2),
                 ('score_t2_3', self.assignment.paper.score_t2_3),
                 ('score_t2_4', self.assignment.paper.score_t2_4),
                 ('score_t2_5', self.assignment.paper.score_t2_5),
                 ("submission_date", self.assignment.paper.submission_date)]),
            "rejected": True,
        })

    def test_chair(self):
        '''Chairs should not be able to update assignments'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_delegate(self):
        '''Delegates should not be able to update assignments'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.assignment.id)
        self.assertEqual(response.data, {
            "id": self.assignment.id,
            "committee": self.assignment.committee.id,
            "country": self.assignment.country.id,
            "registration": self.registration.id,
            "paper": OrderedDict(
                [('id', self.assignment.paper.id),
                 ('file', self.assignment.paper.file),
                 ('graded_file', self.assignment.paper.graded_file),
                 ('graded', self.assignment.paper.graded),
                 ('score_1', self.assignment.paper.score_1),
                 ('score_2', self.assignment.paper.score_2),
                 ('score_3', self.assignment.paper.score_3),
                 ('score_4', self.assignment.paper.score_4),
                 ('score_5', self.assignment.paper.score_5),
                 ('score_t2_1', self.assignment.paper.score_t2_1),
                 ('score_t2_2', self.assignment.paper.score_t2_2),
                 ('score_t2_3', self.assignment.paper.score_t2_3),
                 ('score_t2_4', self.assignment.paper.score_t2_4),
                 ('score_t2_5', self.assignment.paper.score_t2_5),
                 ("submission_date", self.assignment.paper.submission_date)]),
            "rejected": True,
        })


class AssignmentDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:assignment_detail'
    params = {'rejected': True}

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.school = models.new_school(user=self.advisor)
        self.registration = models.new_registration(school=self.school)
        self.chair = models.new_user(
            username='chair', password='chair', user_type=User.TYPE_CHAIR)
        self.committee = models.new_committee(user=self.chair)
        self.assignment = models.new_assignment(
            committee=self.committee, registration=self.registration)
        self.delegate_user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            school=self.school,
            assignment=self.assignment)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update assignments.'''
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It should return correct data.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.assignment.id,
            "committee": self.assignment.committee.id,
            "country": self.assignment.country.id,
            "registration": self.registration.id,
            "paper": OrderedDict(
                [('id', self.assignment.paper.id),
                 ('file', self.assignment.paper.file),
                 ('graded_file', self.assignment.paper.graded_file),
                 ('graded', self.assignment.paper.graded),
                 ('score_1', self.assignment.paper.score_1),
                 ('score_2', self.assignment.paper.score_2),
                 ('score_3', self.assignment.paper.score_3),
                 ('score_4', self.assignment.paper.score_4),
                 ('score_5', self.assignment.paper.score_5),
                 ('score_t2_1', self.assignment.paper.score_t2_1),
                 ('score_t2_2', self.assignment.paper.score_t2_2),
                 ('score_t2_3', self.assignment.paper.score_t2_3),
                 ('score_t2_4', self.assignment.paper.score_t2_4),
                 ('score_t2_5', self.assignment.paper.score_t2_5),
                 ("submission_date", self.assignment.paper.submission_date)]),
            "rejected": True,
        })

    def test_chair(self):
        '''Chairs should not be able to update assignments'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_delegate(self):
        '''Delegates should not be able to update assignments'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.assignment.id)
        self.assertEqual(response.data, {
            "id": self.assignment.id,
            "committee": self.assignment.committee.id,
            "country": self.assignment.country.id,
            "registration": self.registration.id,
            "paper": OrderedDict(
                [('id', self.assignment.paper.id),
                 ('file', self.assignment.paper.file),
                 ('graded_file', self.assignment.paper.graded_file),
                 ('graded', self.assignment.paper.graded),
                 ('score_1', self.assignment.paper.score_1),
                 ('score_2', self.assignment.paper.score_2),
                 ('score_3', self.assignment.paper.score_3),
                 ('score_4', self.assignment.paper.score_4),
                 ('score_5', self.assignment.paper.score_5),
                 ('score_t2_1', self.assignment.paper.score_t2_1),
                 ('score_t2_2', self.assignment.paper.score_t2_2),
                 ('score_t2_3', self.assignment.paper.score_t2_3),
                 ('score_t2_4', self.assignment.paper.score_t2_4),
                 ('score_t2_5', self.assignment.paper.score_t2_5),
                 ("submission_date", self.assignment.paper.submission_date)]),
            "rejected": True,
        })


class AssignmentDetailDeleteTestCase(auto.DestroyAPIAutoTestCase):
    url_name = 'api:assignment_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_assignment()

    def test_anonymous_user(self):
        '''Anonymous users cannot delete assignments.'''
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        '''Advisors cannot delete their assignments.'''
        self.as_user(self.object.registration.school.advisor).do_test(
            expected_error=auto.EXP_DELETE_NOT_ALLOWED)

    def test_chair(self):
        '''Chairs cannot delete their assignments.'''
        chair = models.new_user(user_type=User.TYPE_CHAIR)
        self.as_user(chair).do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_delegate(self):
        '''Delegates cannot delete their assignment.'''
        delegate_user = models.new_user(user_type=User.TYPE_DELEGATE)
        self.as_user(delegate_user).do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_other_user(self):
        '''A user cannot delete another user's assignments.'''
        models.new_school(user=self.default_user)
        self.as_default_user().do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_superuser(self):
        '''A superuser cannot delete assignments.'''
        self.as_superuser().do_test(expected_error=auto.EXP_DELETE_NOT_ALLOWED)


class AssignmentListCreateTestCase(tests.CreateAPITestCase):
    url_name = 'api:assignment_list'
    params = {'rejected': True}

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.chair = models.new_user(
            username='chair', password='chair', user_type=User.TYPE_CHAIR)
        self.school = models.new_school(user=self.advisor)
        self.registration = models.new_registration(school=self.school)
        self.committee = models.new_committee(user=self.chair)
        self.country = models.new_country()
        self.delegate_user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.params['committee'] = self.committee.id
        self.params['registration'] = self.registration.id
        self.params['country'] = self.country.id

    def test_anonymous_user(self):
        '''Anonymous Users should not be able to create assignments.'''
        response = self.get_response(params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors should not be able to create Assignments.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(params=self.params)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Chairs should not be able to create Assignments'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(params=self.params)
        self.assertPermissionDenied(response)

    def test_delegate(self):
        '''Delegates should not be able to create Assignments'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(params=self.params)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''Superusers should be able to create assignments.'''
        models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')

        response = self.get_response(params=self.params)
        response.data.pop('id')
        response.data.pop('paper')
        self.assertEqual(response.data, {
            "committee": self.committee.id,
            "country": self.country.id,
            "registration": self.registration.id,
            "rejected": True,
        })


class AssignmentListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:assignment_list'

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.chair = models.new_user(
            username='chair', password='chair', user_type=User.TYPE_CHAIR)
        self.delegate_user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.school = models.new_school(user=self.advisor)
        self.registration = models.new_registration(school=self.school)
        self.committee = models.new_committee(user=self.chair)
        self.a1 = models.new_assignment(
            registration=self.registration, committee=self.committee)
        self.a2 = models.new_assignment(
            registration=self.registration, committee=self.committee)
        self.a3 = models.new_assignment()

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response()
        self.assertNotAuthenticated(response)

        response = self.get_response(params={'school_id': self.school.id})
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It returns the assignments for the school's advisor.'''
        self.client.login(username='advisor', password='advisor')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(params={'school_id': self.school.id})
        self.assert_assignments_equal(response, [self.a1, self.a2])

    def test_chair(self):
        '''It returns the assignments associated with the chair's committee'''
        self.client.login(username='chair', password='chair')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'committee_id': self.committee.id})
        self.assert_assignments_equal(response, [self.a1, self.a2])

    def test_delegate(self):
        '''Delegates cannot access assignments in bulk.'''
        self.client.login(username='delegate', password='delegate')

        response = self.get_response()
        self.assertPermissionDenied(response)

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = models.new_user(username='another', password='user')
        models.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(params={'school_id': self.school.id})
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It returns the assignments for a superuser.'''
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response()
        self.assert_assignments_equal(response, [self.a1, self.a2, self.a3])

        response = self.get_response(params={'school_id': self.school.id})
        self.assert_assignments_equal(response, [self.a1, self.a2])

    def assert_assignments_equal(self, response, assignments):
        '''Assert that the response contains the assignments in order.'''
        self.assertEqual(response.data, [{
            'id': a.id,
            'country': a.country_id,
            'committee': a.committee_id,
            'registration': a.registration_id,
            "paper": OrderedDict(
                [('id', a.paper.id), ('file', a.paper.file),
                 ('graded_file', a.paper.graded_file),
                 ('graded', a.paper.graded), ('score_1', a.paper.score_1),
                 ('score_2', a.paper.score_2), ('score_3', a.paper.score_3),
                 ('score_4', a.paper.score_4), ('score_5', a.paper.score_5),
                 ('score_t2_1', a.paper.score_t2_1),
                 ('score_t2_2', a.paper.score_t2_2),
                 ('score_t2_3', a.paper.score_t2_3),
                 ('score_t2_4', a.paper.score_t2_4),
                 ('score_t2_5', a.paper.score_t2_5),
                 ('submission_date', a.paper.submission_date)]),
            'rejected': a.rejected,
        } for a in assignments])
