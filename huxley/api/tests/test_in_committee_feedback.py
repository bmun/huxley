# copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.exceptions import ValidationError

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models
import random

class InCommitteeFeedbackDetailGetTestCase(tests.RetrieveAPITestCase):
    url_name = 'api:in_committee_feedback_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_in_committee_feedback()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        advisor = models.new_user(user_type=User.TYPE_ADVISOR)
        self.as_user(advisor).do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_chair(self):
        chair = models.new_user(user_type=User.TYPE_CHAIR)
        self.as_user(chair).do_test()

    def test_delegate(self):
        delegate = models.new_user(user_type=User.TYPE_DELEGATE)
        self.as_user(delegate).do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_superuser(self):
        self.as_superuser().do_test()


class InCommitteeFeedbackDetailPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:in_committee_feedback_detail'

    def setUp(self):
        self.committee = models.new_committee(name='CYBER')
        self.assignment = models.new_assignment(committee=self.committee)
        self.feedback = models.new_in_committee_feedback(assignment=self.assignment)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update feedback.'''
        response = self.get_response(self.feedback.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors should not be able to update feedback.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.feedback.id)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Chairs should be able to update feedback'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.feedback.id)
        self.assertEqual(response.data, {
            "id": self.feedback.id,
            "feedback": self.feedback.feedback,
            "assignment": self.assignment.id,
            "score": self.feedback.score,
            "speech": self.feedback.speech.id,
            })

    def test_delegate(self):
        '''Delegates should not be able to update feedback'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.feedback.id)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''Should return correct data; superusers should be able to update feedback'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.feedback.id)
        self.assertEqual(response.data, {
            "id": self.feedback.id,
            "feedback": self.feedback.feedback,
            "assignment": self.assignment.id,
            "score": self.feedback.score,
            "speech": self.feedback.speech.id,
            })


class InCommitteeFeedbackDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:in_committee_feedback_detail'

    def setUp(self):
        self.committee = models.new_committee(name='CYBER')
        self.assignment = models.new_assignment(committee=self.committee)
        self.feedback = models.new_in_committee_feedback(assignment=self.assignment)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update feedback.'''
        response = self.get_response(self.feedback.id)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors should not be able to update feedback.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.feedback.id)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Should return correct data; chairs should be able to update feedback'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.feedback.id)
        self.assertEqual(response.data, {
            "id": self.feedback.id,
            "feedback": self.feedback.feedback,
            "assignment": self.assignment.id,
            "score": self.feedback.score,
            "speech": self.feedback.speech.id,
            })

    def test_delegate(self):
        '''Delegates should not be able to update feedback'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.feedback.id)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''Should return correct data; superusers should be able to update feedback'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.feedback.id)
        self.assertEqual(response.data, {
            "id": self.feedback.id,
            "feedback": self.feedback.feedback,
            "assignment": self.assignment.id,
            "score": self.feedback.score,
            "speech": self.feedback.speech.id,
            })

class InCommitteeFeedbackListCreateTestCase(tests.CreateAPITestCase):
    url_name = 'api:in_committee_feedback_list'

    def setUp(self):
        self.committee = models.new_committee(name='CYBER')
        self.assignment1 = models.new_assignment(committee=self.committee)
        self.assignment2 = models.new_assignment()
        self.feedback1 = models.new_in_committee_feedback(assignment=self.assignment1)
        self.feedback2 = models.new_in_committee_feedback(assignment=self.assignment1)
        self.feedback3 = models.new_in_committee_feedback(assignment=self.assignment2)

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response()
        self.assertNotAuthenticated(response)

        response = self.get_response(params={'assignment_id': self.assignment1.id})
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors cannot access in-committee feedback.'''
        self.client.login(username='advisor', password='advisor')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''It returns the feedback associated with the assignment the chair is looking up.'''
        self.client.login(username='chair', password='chair')

        response = self.get_response()
        self.assert_feedbacks_equal(response, [self.feedback1, self.feedback2, self.feedback3])

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assert_feedbacks_equal(response, [self.feedback1, self.feedback2])

    def test_delegate(self):
        '''Delegates cannot access in-committee feedback.'''
        self.client.login(username='delegate', password='delegate')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assertPermissionDenied(response)

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = models.new_user(username='another', password='user')
        models.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It returns the feedback associated with the assignment the superuser is looking up.'''
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response()
        self.assert_assignments_equal(response, [self.feedback1, self.feedback2, self.feedback3])

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assert_feedbacks_equal(response, [self.feedback1, self.feedback2])

    def assert_feedbacks_equal(self, response, feedbacks):
        '''Assert that the response contains the feedback in order.'''
        self.assertEqual(response.data, [{
            'id': f.id,
            'feedback': f.feedback,
            'assignment': f.assignment.id,
            'score': f.score,
            'speech': f.speech.id,
        } for f in feedbacks])

class InCommitteeFeedbackListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:in_committee_feedback_list'

    def setUp(self):
        self.committee = models.new_committee(name='CYBER')
        self.assignment1 = models.new_assignment(committee=self.committee)
        self.assignment2 = models.new_assignment()
        self.feedback1 = models.new_in_committee_feedback(assignment=self.assignment1)
        self.feedback2 = models.new_in_committee_feedback(assignment=self.assignment1)
        self.feedback3 = models.new_in_committee_feedback(assignment=self.assignment2)

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response()
        self.assertNotAuthenticated(response)

        response = self.get_response(params={'assignment_id': self.assignment1.id})
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors cannot access in-committee feedback.'''
        self.client.login(username='advisor', password='advisor')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''It returns the feedback associated with the assignment the chair is looking up.'''
        self.client.login(username='chair', password='chair')

        response = self.get_response()
        self.assert_feedbacks_equal(response, [self.feedback1, self.feedback2, self.feedback3])

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assert_feedbacks_equal(response, [self.feedback1, self.feedback2])

    def test_delegate(self):
        '''Delegates cannot access in-committee feedback.'''
        self.client.login(username='delegate', password='delegate')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assertPermissionDenied(response)

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = models.new_user(username='another', password='user')
        models.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It returns the feedback associated with the assignment the superuser is looking up.'''
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response()
        self.assert_assignments_equal(response, [self.feedback1, self.feedback2, self.feedback3])

        response = self.get_response(
            params={'assignment_id': self.assignment1.id})
        self.assert_feedbacks_equal(response, [self.feedback1, self.feedback2])

    def assert_feedbacks_equal(self, response, feedbacks):
        '''Assert that the response contains the feedback in order.'''
        self.assertEqual(response.data, [{
            'id': f.id,
            'feedback': f.feedback,
            'assignment': f.assignment.id,
            'score': f.score,
            'speech': f.speech.id,
        } for f in feedbacks])


