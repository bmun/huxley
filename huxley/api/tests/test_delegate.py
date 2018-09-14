# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.exceptions import ValidationError

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models


class DelegateDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:delegate_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_delegate()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        self.as_user(self.object.school.advisor).do_test()

    def test_chair(self):
        chair = models.new_user(
            user_type=User.TYPE_CHAIR,
            committee=self.object.assignment.committee)
        self.as_user(chair).do_test()

    def test_delegate(self):
        delegate_1 = models.new_user(user_type=User.TYPE_DELEGATE)
        self.as_user(delegate_1).do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

        delegate_2 = models.new_user(
            user_type=User.TYPE_DELEGATE, delegate=self.object)
        self.as_user(delegate_2).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()


class DelegateDetailPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:delegate_detail'
    params = {
        'name': 'Trevor Dowds',
        'email': 'tdowds@hotmail.org',
        'summary': 'He did awful!',
        'published_summary': 'He moderately underperformed expectations.'
    }

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
        self.assignment = models.new_assignment(
            registration=self.registration, committee=self.committee)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            assignment=self.assignment,
            school=self.school)
        self.params['assignment'] = self.assignment.id

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update delegates.'''
        response = self.get_response(self.delegate.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It should return correct data.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id": self.delegate.id,
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": self.delegate.voting,
            "session_one": self.delegate.session_one,
            "session_two": self.delegate.session_two,
            "session_three": self.delegate.session_three,
            "session_four": self.delegate.session_four,
            "committee_feedback_submitted":
            self.delegate.committee_feedback_submitted,
            "waiver_submitted": self.delegate.waiver_submitted
        })

    def test_chair(self):
        '''It should return correct data.'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id": self.delegate.id,
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": self.delegate.voting,
            "session_one": self.delegate.session_one,
            "session_two": self.delegate.session_two,
            "session_three": self.delegate.session_three,
            "session_four": self.delegate.session_four,
            "committee_feedback_submitted":
            self.delegate.committee_feedback_submitted,
            "waiver_submitted": self.delegate.waiver_submitted
        })

    def test_delegate(self):
        '''It should return correct data.'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id": self.delegate.id,
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": self.delegate.voting,
            "session_one": self.delegate.session_one,
            "session_two": self.delegate.session_two,
            "session_three": self.delegate.session_three,
            "session_four": self.delegate.session_four,
            "committee_feedback_submitted":
            self.delegate.committee_feedback_submitted,
            "waiver_submitted": self.delegate.waiver_submitted
        })

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id": self.delegate.id,
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": self.delegate.voting,
            "session_one": self.delegate.session_one,
            "session_two": self.delegate.session_two,
            "session_three": self.delegate.session_three,
            "session_four": self.delegate.session_four,
            "committee_feedback_submitted":
            self.delegate.committee_feedback_submitted,
            "waiver_submitted": self.delegate.waiver_submitted
        })


class DelegateDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:delegate_detail'
    params = {
        'name': 'Trevor Dowds',
        'email': 'tdowds@hotmail.org',
        'summary': 'He did awful!',
        'published_summary': 'He moderately underperformed expectations.'
    }

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
        self.assignment = models.new_assignment(
            registration=self.registration, committee=self.committee)
        self.delegate = models.new_delegate(
            user=self.delegate_user,
            assignment=self.assignment,
            school=self.school)

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update assignments.'''
        response = self.get_response(self.delegate.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It should return correct data allowing a partial update.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id": self.delegate.id,
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": self.delegate.voting,
            "session_one": self.delegate.session_one,
            "session_two": self.delegate.session_two,
            "session_three": self.delegate.session_three,
            "session_four": self.delegate.session_four,
            "committee_feedback_submitted":
            self.delegate.committee_feedback_submitted,
            "waiver_submitted": self.delegate.waiver_submitted
        })

    def test_chair(self):
        '''It should return correct data allowing a partial update.'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id": self.delegate.id,
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": self.delegate.voting,
            "session_one": self.delegate.session_one,
            "session_two": self.delegate.session_two,
            "session_three": self.delegate.session_three,
            "session_four": self.delegate.session_four,
            "committee_feedback_submitted":
            self.delegate.committee_feedback_submitted,
            "waiver_submitted": self.delegate.waiver_submitted
        })

    def test_delegate(self):
        '''It should return correct data allowing a partial update.'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id": self.delegate.id,
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": self.delegate.voting,
            "session_one": self.delegate.session_one,
            "session_two": self.delegate.session_two,
            "session_three": self.delegate.session_three,
            "session_four": self.delegate.session_four,
            "committee_feedback_submitted":
            self.delegate.committee_feedback_submitted,
            "waiver_submitted": self.delegate.waiver_submitted
        })

    def test_superuser(self):
        '''It should return correct data allowing a partial update.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.delegate.id, params=self.params)
        response.data.pop('created_at')
        self.assertEqual(response.data, {
            "id": self.delegate.id,
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": self.delegate.voting,
            "session_one": self.delegate.session_one,
            "session_two": self.delegate.session_two,
            "session_three": self.delegate.session_three,
            "session_four": self.delegate.session_four,
            "committee_feedback_submitted":
            self.delegate.committee_feedback_submitted,
            "waiver_submitted": self.delegate.waiver_submitted
        })


class DelegateDetailDeleteTestCase(auto.DestroyAPIAutoTestCase):
    url_name = 'api:delegate_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_delegate()

    def test_anonymous_user(self):
        '''Anonymous users cannot delete delegates.'''
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        '''Advisors can delete their delegates.'''
        self.as_user(self.object.school.advisor).do_test()

    def test_chair(self):
        '''Chairs cannot delete their delegates.'''
        chair = models.new_user(user_type=User.TYPE_CHAIR)
        self.as_user(chair).do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_delegate(self):
        '''Delegates cannot delete their associated delegate model.'''
        delegate = models.new_user(user_type=User.TYPE_DELEGATE)
        self.as_user(delegate).do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_other_user(self):
        '''A user cannot delete another user's delegates.'''
        models.new_school(user=self.default_user)
        self.as_default_user().do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_superuser(self):
        '''A superuser can delete delegates.'''
        self.as_superuser().do_test()


class DelegateListCreateTestCase(tests.CreateAPITestCase):
    url_name = 'api:delegate_list'
    params = {
        'name': 'Trevor Dowds',
        'email': 'tdowds@hotmail.org',
        'summary': 'He did awful!',
        'published_summary': 'He moderately underperformed expectations.'
    }

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.advisor2 = models.new_user(
            username='advisor2', password='advisor2')
        self.chair = models.new_user(
            username='chair', password='chair', user_type=User.TYPE_CHAIR)
        self.delegate_user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.school = models.new_school(user=self.advisor)
        self.school2 = models.new_school(user=self.advisor2)
        self.registration = models.new_registration(school=self.school)
        self.registration2 = models.new_registration(school=self.school2)
        self.committee = models.new_committee(user=self.chair)
        self.assignment = models.new_assignment(
            registration=self.registration, committee=self.committee)
        self.params['assignment'] = self.assignment.id
        self.params['school'] = self.school.id

    def test_anonymous_user(self):
        '''Anonymous users can't create delegates.'''
        response = self.get_response(params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Should allow advisors to create new delegates.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(params=self.params)
        response.data.pop('created_at')
        response.data.pop('id')
        self.assertEqual(response.data, {
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": False,
            "session_one": False,
            "session_two": False,
            "session_three": False,
            "session_four": False,
            "committee_feedback_submitted": False,
            "waiver_submitted": False
        })

    def test_chair(self):
        '''Chairs should not be able to create delegates'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(params=self.params)
        self.assertPermissionDenied(response)

    def test_delegate(self):
        '''Delegates should not be able to create delegates'''
        self.client.login(username='delegate', password='delegate')
        response = self.get_response(params=self.params)
        self.assertPermissionDenied(response)

    def test_other_advisor(self):
        '''Should not allow other advisor to create new delegates.'''
        self.client.login(username='advisor2', password='advisor2')
        response = self.get_response(params=self.params)
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''Should allow superuser to create delegate.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(params=self.params)
        response.data.pop('created_at')
        response.data.pop('id')
        self.assertEqual(response.data, {
            "assignment": self.assignment.id,
            "school": self.school.id,
            "name": unicode(self.params['name']),
            "email": unicode(self.params['email']),
            "summary": unicode(self.params['summary']),
            "published_summary": unicode(self.params['published_summary']),
            "voting": False,
            "session_one": False,
            "session_two": False,
            "session_three": False,
            "session_four": False,
            "committee_feedback_submitted": False,
            "waiver_submitted": False
        })


class DelegateListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:delegate_list'

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
        self.assignment1 = models.new_assignment(
            registration=self.registration, committee=self.committee)
        self.assignment2 = models.new_assignment(
            registration=self.registration)
        self.delegate1 = models.new_delegate(assignment=self.assignment1, )
        self.delegate2 = models.new_delegate(
            assignment=self.assignment2,
            name='Trevor Dowds',
            email='t@dowds.com',
            summary='Good!')

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response(params={'school_id': self.school.id})
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It returns the delegates for the school's advisor.'''
        self.client.login(username='advisor', password='advisor')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(params={'school_id': self.school.id})
        self.assert_delegates_equal(response, [self.delegate1, self.delegate2])

    def test_chair(self):
        '''It returns the delegates associated with a chair's committee'''
        self.client.login(username='chair', password='chair')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'committee_id': self.committee.id})
        self.assert_delegates_equal(response, [self.delegate1])

    def test_delegate(self):
        '''Delegates cannot retrieve delegates in bulk.'''
        self.client.login(username='delegate', password='delegate')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(params={'school_id': self.school.id})
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'committee_id': self.committee.id})
        self.assertPermissionDenied(response)

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = models.new_user(username='another', password='user')
        models.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response(params={'school_id': self.school.id})
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It returns the delegates for a superuser.'''
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response(params={'school_id': self.school.id})
        self.assert_delegates_equal(response, [self.delegate1, self.delegate2])

    def assert_delegates_equal(self, response, delegates):
        '''Assert the response contains each of the delegates'''
        self.assertEqual(len(response.data), len(delegates))

        for i in range(len(response.data)):
            self.assertEqual(
                dict(response.data[i]), {
                    'id': delegates[i].id,
                    'assignment': delegates[i].assignment.id,
                    'school': delegates[i].school.id,
                    'name': unicode(delegates[i].name),
                    'email': unicode(delegates[i].email),
                    'summary': unicode(delegates[i].summary),
                    'published_summary':
                    unicode(delegates[i].published_summary),
                    'created_at': delegates[i].created_at.isoformat(),
                    "voting": delegates[i].voting,
                    'session_one': delegates[i].session_one,
                    'session_two': delegates[i].session_two,
                    'session_three': delegates[i].session_three,
                    'session_four': delegates[i].session_four,
                    'committee_feedback_submitted':
                    delegates[i].committee_feedback_submitted,
                    'waiver_submitted': delegates[i].waiver_submitted
                })


class DelegateListPartialUpdateTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:delegate_list'
    is_resource = False

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.advisor2 = models.new_user(
            username='advisor2', password='advisor')
        self.chair = models.new_user(
            username='chair', password='chair', user_type=User.TYPE_CHAIR)
        self.delegate_user = models.new_user(
            username='delegate',
            password='delegate',
            user_type=User.TYPE_DELEGATE)
        self.school = models.new_school(user=self.advisor)
        self.school2 = models.new_school(user=self.advisor2)
        self.registration = models.new_registration(school=self.school)
        self.registration2 = models.new_registration(school=self.school2)
        self.committee = models.new_committee(user=self.chair)

        self.assignment1 = models.new_assignment(
            registration=self.registration, committee=self.committee)
        self.assignment2 = models.new_assignment(
            registration=self.registration)
        self.assignment3 = models.new_assignment(
            registration=self.registration2, committee=self.committee)
        self.new_assignment = models.new_assignment(
            registration=self.registration)
        self.new_assignment2 = models.new_assignment(
            registration=self.registration2)
        self.faulty_assignment = models.new_assignment()

        self.delegate1 = models.new_delegate(
            name="Nathaniel Parke",
            school=self.school,
            assignment=self.assignment1)

        self.delegate2 = models.new_delegate(
            name='Trevor Dowds',
            school=self.school,
            assignment=self.assignment2)

        self.delegate3 = models.new_delegate(
            name='Kunal Mehta',
            school=self.school2,
            assignment=self.assignment3)

        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.new_assignment.id}, {'id': self.delegate2.id,
                                                     'assignment': None}
        ]

    def test_anonymous_user(self):
        '''Rejects partial update from an anonymous user.'''
        response = self.get_response()
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It updates the delegates for the school's advisor.'''
        self.client.login(username='advisor', password='advisor')

        response = self.get_response()
        self.assertEqual(
            dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.params[0]['assignment'],
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'published_summary': unicode(self.delegate1.published_summary),
                'created_at': self.delegate1.created_at.isoformat(),
                'voting': self.delegate1.voting,
                "session_one": self.delegate1.session_one,
                "session_two": self.delegate1.session_two,
                "session_three": self.delegate1.session_three,
                "session_four": self.delegate1.session_four,
                "committee_feedback_submitted":
                self.delegate1.committee_feedback_submitted,
                "waiver_submitted": self.delegate1.waiver_submitted
            }, )
        self.assertEqual(
            dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.params[1]['assignment'],
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
                'published_summary': unicode(self.delegate2.published_summary),
                'created_at': self.delegate2.created_at.isoformat(),
                'voting': self.delegate2.voting,
                "session_one": self.delegate2.session_one,
                "session_two": self.delegate2.session_two,
                "session_three": self.delegate2.session_three,
                "session_four": self.delegate2.session_four,
                "committee_feedback_submitted":
                self.delegate2.committee_feedback_submitted,
                "waiver_submitted": self.delegate2.waiver_submitted
            }, )

    def test_advisor_fail(self):
        '''
        It doesn't update the delegates for the school's advisor if fields
        are invalid.
        '''
        self.client.login(username='advisor', password='advisor')
        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.faulty_assignment.id},
            {'id': self.delegate2.id,
             'assignment': self.new_assignment.id}
        ]

        self.assertRaises(ValidationError, self.get_response, self.school.id)

    def test_chair(self):
        '''It updates the delegates for the chair's committee'''
        self.client.login(username='chair', password='chair')
        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.new_assignment.id}, {'id': self.delegate3.id,
                                                     'assignment':
                                                     self.new_assignment2.id}
        ]
        response = self.get_response()

        self.assertEqual(
            dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.params[0]['assignment'],
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'published_summary': unicode(self.delegate1.published_summary),
                'created_at': self.delegate1.created_at.isoformat(),
                'voting': self.delegate1.voting,
                "session_one": self.delegate1.session_one,
                "session_two": self.delegate1.session_two,
                "session_three": self.delegate1.session_three,
                "session_four": self.delegate1.session_four,
                "committee_feedback_submitted":
                self.delegate1.committee_feedback_submitted,
                "waiver_submitted": self.delegate1.waiver_submitted
            }, )
        self.assertEqual(
            dict(response.data[1]),
            {
                'id': self.delegate3.id,
                'assignment': self.params[1]['assignment'],
                'school': self.delegate3.school.id,
                'name': unicode(self.delegate3.name),
                'email': unicode(self.delegate3.email),
                'summary': unicode(self.delegate3.summary),
                'published_summary': unicode(self.delegate3.published_summary),
                'created_at': self.delegate3.created_at.isoformat(),
                'voting': self.delegate3.voting,
                "session_one": self.delegate3.session_one,
                "session_two": self.delegate3.session_two,
                "session_three": self.delegate3.session_three,
                "session_four": self.delegate3.session_four,
                "committee_feedback_submitted":
                self.delegate3.committee_feedback_submitted,
                "waiver_submitted": self.delegate3.waiver_submitted
            }, )

    def test_chair_fail(self):
        '''
        It doesn't update the delegates for the committee's chair if fields
        are invalid.
        '''
        self.client.login(username='chair', password='chair')
        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.faulty_assignment.id},
            {'id': self.delegate3.id,
             'assignment': self.new_assignment2.id}
        ]

        self.assertRaises(ValidationError, self.get_response,
                          self.committee.id)

    def test_delegate(self):
        '''Should reject a partial update from a delegate.'''
        self.client.login(username='delegate', password='delegate')

        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.new_assignment.id}, {'id': self.delegate2.id,
                                                     'assignment': None},
            {'id': self.delegate3.id,
             'assignment': None}
        ]

        response = self.get_response()
        self.assertPermissionDenied(response)

    def test_other_user(self):
        '''Should reject a partial update from another user.'''
        self.client.login(username='advisor2', password='advisor')

        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.new_assignment.id}, {'id': self.delegate2.id,
                                                     'assignment': None},
            {'id': self.delegate3.id,
             'assignment': None}
        ]

        response = self.get_response()
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It updates the delegates for a superuser.'''
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response(self.school.id)
        self.assertEqual(
            dict(response.data[0]),
            {
                'id': self.delegate1.id,
                'assignment': self.params[0]['assignment'],
                'school': self.delegate1.school.id,
                'name': unicode(self.delegate1.name),
                'email': unicode(self.delegate1.email),
                'summary': unicode(self.delegate1.summary),
                'published_summary': unicode(self.delegate1.published_summary),
                'created_at': self.delegate1.created_at.isoformat(),
                'voting': self.delegate1.voting,
                "session_one": self.delegate1.session_one,
                "session_two": self.delegate1.session_two,
                "session_three": self.delegate1.session_three,
                "session_four": self.delegate1.session_four,
                "committee_feedback_submitted":
                self.delegate1.committee_feedback_submitted,
                "waiver_submitted": self.delegate1.waiver_submitted
            }, )
        self.assertEqual(
            dict(response.data[1]),
            {
                'id': self.delegate2.id,
                'assignment': self.params[1]['assignment'],
                'school': self.delegate2.school.id,
                'name': unicode(self.delegate2.name),
                'email': unicode(self.delegate2.email),
                'summary': unicode(self.delegate2.summary),
                'published_summary': unicode(self.delegate2.published_summary),
                'created_at': self.delegate2.created_at.isoformat(),
                'voting': self.delegate2.voting,
                "session_one": self.delegate2.session_one,
                "session_two": self.delegate2.session_two,
                "session_three": self.delegate2.session_three,
                "session_four": self.delegate2.session_four,
                "committee_feedback_submitted":
                self.delegate2.committee_feedback_submitted,
                "waiver_submitted": self.delegate2.waiver_submitted
            }, )

    def test_superuser_fail(self):
        '''
        It doesn't update the delegates for the superuser if fields are invalid.
        '''
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')
        self.params = [
            {'id': self.delegate1.id,
             'assignment': self.faulty_assignment.id},
            {'id': self.delegate2.id,
             'assignment': self.new_assignment.id}
        ]

        self.assertRaises(ValidationError, self.get_response, self.school.id)
