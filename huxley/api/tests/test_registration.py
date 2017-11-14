# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.core.models import Conference, Registration
from huxley.utils.test import models


class RegistrationListPostTest(tests.CreateAPITestCase):
    url_name = 'api:registration_list'
    params = {
        'num_beginner_delegates': 0,
        'num_intermediate_delegates': 0,
        'num_advanced_delegates': 0,
        'num_spanish_speaking_delegates': 0,
        'num_chinese_speaking_delegates': 0,
        'country_preferences': [1, 2]
    }

    def test_valid(self):
        school = models.new_school()
        conference = Conference.get_current()
        params = self.get_params()
        params['school'] = school.id
        params['conference'] = conference.session

        response = self.get_response(params=params)

        registration_query = Registration.objects.filter(
            id=response.data['id'])
        self.assertTrue(registration_query.exists())

        registration = Registration.objects.get(id=response.data['id'])
        self.assertEqual(response.data, {
            'id': registration.id,
            'registered_at': registration.registered_at.isoformat(),
            'school': registration.school.id,
            'conference': registration.conference.session,
            'is_waitlisted': registration.is_waitlisted,
            'num_beginner_delegates': registration.num_beginner_delegates,
            'num_intermediate_delegates':
            registration.num_intermediate_delegates,
            'num_advanced_delegates': registration.num_advanced_delegates,
            'num_spanish_speaking_delegates':
            registration.num_spanish_speaking_delegates,
            'num_chinese_speaking_delegates':
            registration.num_chinese_speaking_delegates,
            'waivers_completed': registration.waivers_completed,
            'country_preferences': registration.country_preference_ids,
            'registration_comments': registration.registration_comments,
            'committee_preferences':
            list(registration.committee_preferences.all()),
            'delegate_fees_owed': float(registration.delegate_fees_owed),
            'delegate_fees_paid': float(registration.delegate_fees_paid),
            'registration_fee_paid': registration.registration_fee_paid,
            'assignments_finalized': registration.assignments_finalized,
            'modified_at': registration.modified_at.isoformat(),
        })

    def test_empty_fields(self):
        '''This should not allow for required fields to be empty.'''
        params = self.get_params(
            num_beginner_delegates='',
            num_intermediate_delegates='',
            num_advanced_delegates='',
            num_spanish_speaking_delegates='',
            num_chinese_speaking_delegates='')
        response = self.get_response(params=params)

        self.assertEqual(
            response.data,
            {'num_beginner_delegates': [u'A valid integer is required.'],
             'num_advanced_delegates': [u'A valid integer is required.'],
             'num_chinese_speaking_delegates':
             [u'A valid integer is required.'],
             'num_intermediate_delegates': [u'A valid integer is required.'],
             'num_spanish_speaking_delegates':
             [u'A valid integer is required.'],
             'conference': [u'This field is required.'],
             'school': [u'This field is required.']})

    def test_fees(self):
        '''Fees should be read-only fields.'''
        school = models.new_school()
        conference = Conference.get_current()
        params = self.get_params(
            school=school.id,
            conference=conference.session,
            fees_owed=2000.0,
            fees_paid=2000.0)
        response = self.get_response(params=params)

        registration = Registration.objects.get(id=response.data['id'])
        delegate_fees_owed = response.data['delegate_fees_owed']
        delegate_fees_paid = response.data['delegate_fees_paid']

        self.assertEqual(delegate_fees_owed, float(registration.delegate_fees_owed))
        self.assertEqual(delegate_fees_paid, float(registration.delegate_fees_paid))
        self.assertNotEqual(delegate_fees_owed, 2000.0)
        self.assertNotEqual(delegate_fees_paid, 2000.0)

    def test_country_preferences(self):
        '''It should save country preferences.'''
        c1 = models.new_country().id
        c2 = models.new_country().id
        school = models.new_school()
        conference = Conference.get_current()
        params = self.get_params(
            school=school.id,
            conference=conference.session,
            countrypreferences=[0, c1, c2, 0, c1])
        response = self.get_response(params=params)

        self.assertEqual(response.data['country_preferences'], [c1, c2])

        registration_id = response.data['id']
        registration = Registration.objects.get(id=registration_id)
        self.assertEqual([c1, c2], registration.country_preference_ids)

    # def test_delegate_total(self):
    #     '''Validator shouldn't let there be more spanish or chinese speaking
    #  delegates than there are total delegates.'''
    #     school = models.new_school()
    #     conference = Conference.get_current()
    #     params = self.get_params(
    #         school=school.id,
    #         conference=conference.session,
    #         num_beginner_delegates=1,
    #         num_intermediate_delegates=1,
    #         num_advanced_delegates=1,
    #         num_spanish_speaking_delegates=4,
    #         num_chinese_speaking_delegates=4)

    #     response = self.get_response(params=params)
    #     self.assertEqual(response.data,
    #                      {'num_spanish_speaking_delegates':
    #                       [u'Cannot exceed total number of delegates.'],
    #                       'num_chinese_speaking_delegates':
    #                       [u'Cannot exceed total number of delegates.']})


class RegistrationListGetTest(tests.ListAPITestCase):
    url_name = 'api:registration_list'

    def setUp(self):
        self.advisor = models.new_user(username='username', password='pass')
        self.school = models.new_school(user=self.advisor)
        self.registration = models.new_registration(school=self.school)

    def test_anonymous_user(self):
        response = self.get_response({'school_id': self.school.id,
                                      'conference_session':
                                      Conference.get_current()})
        self.assertNotAuthenticated(response)

        response = self.get_response()
        self.assertNotAuthenticated(response)

    def test_other_user(self):
        other_user = models.new_user(username='other', password='other')
        other_school = models.new_school(user=other_user)
        self.client.login(username='other', password='other')
        response = self.get_response(params={'school_id': self.school.id,
                                             'conference_session':
                                             Conference.get_current()})
        self.assertPermissionDenied(response)

        response = self.get_response()
        self.assertPermissionDenied(response)

    def test_advisor(self):
        self.client.login(username='username', password='pass')
        response = self.get_response(params={'school_id': self.school.id,
                                             'conference_session':
                                             Conference.get_current()})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            dict(response.data[0]), {
                'id': self.registration.id,
                'school': self.registration.school_id,
                'conference': self.registration.conference_id,
                'registered_at': self.registration.registered_at.isoformat(),
                'is_waitlisted': self.registration.is_waitlisted,
                'num_beginner_delegates':
                self.registration.num_beginner_delegates,
                'num_intermediate_delegates':
                self.registration.num_intermediate_delegates,
                'num_advanced_delegates':
                self.registration.num_advanced_delegates,
                'num_spanish_speaking_delegates':
                self.registration.num_spanish_speaking_delegates,
                'num_chinese_speaking_delegates':
                self.registration.num_chinese_speaking_delegates,
                'waivers_completed': self.registration.waivers_completed,
                'country_preferences':
                self.registration.country_preference_ids,
                'committee_preferences':
                list(self.registration.committee_preferences.all()),
                'registration_comments':
                self.registration.registration_comments,
                'delegate_fees_owed': float(self.registration.delegate_fees_owed),
                'delegate_fees_paid': float(self.registration.delegate_fees_paid),
                'registration_fee_paid': self.registration.registration_fee_paid,
                'assignments_finalized':
                self.registration.assignments_finalized,
                'modified_at': self.registration.modified_at.isoformat()
            })

    def test_superuser(self):
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')
        response = self.get_response(params={'school_id': self.school.id,
                                             'conference_session':
                                             Conference.get_current()})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            dict(response.data[0]), {
                'id': self.registration.id,
                'school': self.registration.school_id,
                'conference': self.registration.conference_id,
                'registered_at': self.registration.registered_at.isoformat(),
                'is_waitlisted': self.registration.is_waitlisted,
                'num_beginner_delegates':
                self.registration.num_beginner_delegates,
                'num_intermediate_delegates':
                self.registration.num_intermediate_delegates,
                'num_advanced_delegates':
                self.registration.num_advanced_delegates,
                'num_spanish_speaking_delegates':
                self.registration.num_spanish_speaking_delegates,
                'num_chinese_speaking_delegates':
                self.registration.num_chinese_speaking_delegates,
                'waivers_completed': self.registration.waivers_completed,
                'country_preferences':
                self.registration.country_preference_ids,
                'committee_preferences':
                list(self.registration.committee_preferences.all()),
                'registration_comments':
                self.registration.registration_comments,
                'delegate_fees_owed': float(self.registration.delegate_fees_owed),
                'delegate_fees_paid': float(self.registration.delegate_fees_paid),
                'registration_fee_paid': self.registration.registration_fee_paid,
                'assignments_finalized':
                self.registration.assignments_finalized,
                'modified_at': self.registration.modified_at.isoformat()
            })


class RegistrationDetailGetTest(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:registration_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_registration()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_other_user(self):
        other_user = models.new_user()
        school = models.new_school(user=other_user)
        self.as_user(other_user).do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_advisor(self):
        advisor = User.objects.get(school_id=self.object.school_id)
        advisor.PASSWORD_FOR_TESTS_ONLY = 'test'
        self.as_user(advisor).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()


class RegistrationDetailPutTest(tests.UpdateAPITestCase):
    url_name = 'api:registration_detail'

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.school = models.new_school(user=self.advisor)
        self.registration = models.new_registration(school=self.school)
        self.params = {
            'conference': self.registration.conference.session,
            'school': self.registration.school.id,
            'country_preferences': self.registration.country_preference_ids,
            'assignments_finalized': True
        }

    def test_anonymous_user(self):
        '''Anonymous user should not be able to submit a full update.'''
        response = self.get_response(self.registration.id, self.params)
        self.assertNotAuthenticated(response)

    def test_other_user(self):
        '''A user should not be able to fully update another user's info.'''
        other_user = models.new_user(username='username', password='password')
        school = models.new_school(user=other_user)
        self.client.login(username='username', password='password')
        response = self.get_response(self.registration.id, self.params)
        self.assertPermissionDenied(response)

    def test_advisor(self):
        '''An advisor should be able to fully update his/her info.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.registration.id, self.params)
        self.assertEqual(response.data, {
            'id': self.registration.id,
            'school': self.registration.school.id,
            'conference': self.registration.conference.session,
            'registered_at': self.registration.registered_at.isoformat(),
            'is_waitlisted': self.registration.is_waitlisted,
            'num_beginner_delegates': self.registration.num_beginner_delegates,
            'num_intermediate_delegates':
            self.registration.num_intermediate_delegates,
            'num_advanced_delegates': self.registration.num_advanced_delegates,
            'num_spanish_speaking_delegates':
            self.registration.num_spanish_speaking_delegates,
            'num_chinese_speaking_delegates':
            self.registration.num_chinese_speaking_delegates,
            'waivers_completed': self.registration.waivers_completed,
            'country_preferences': self.registration.country_preference_ids,
            'committee_preferences':
            list(self.registration.committee_preferences.all()),
            'registration_comments': self.registration.registration_comments,
            'delegate_fees_owed': float(self.registration.delegate_fees_owed),
            'delegate_fees_paid': float(self.registration.delegate_fees_paid),
            'registration_fee_paid': self.registration.registration_fee_paid,
            'assignments_finalized': True,
            'modified_at': self.registration.modified_at.isoformat()
        })

    def test_superuser(self):
        '''A superuser should be able to fully update anyone's info.'''
        models.new_superuser(username='super', password='user')
        self.client.login(username='super', password='user')
        response = self.get_response(self.registration.id, self.params)
        self.assertEqual(response.data, {
            'id': self.registration.id,
            'school': self.registration.school.id,
            'conference': self.registration.conference.session,
            'registered_at': self.registration.registered_at.isoformat(),
            'is_waitlisted': self.registration.is_waitlisted,
            'num_beginner_delegates': self.registration.num_beginner_delegates,
            'num_intermediate_delegates':
            self.registration.num_intermediate_delegates,
            'num_advanced_delegates': self.registration.num_advanced_delegates,
            'num_spanish_speaking_delegates':
            self.registration.num_spanish_speaking_delegates,
            'num_chinese_speaking_delegates':
            self.registration.num_chinese_speaking_delegates,
            'waivers_completed': self.registration.waivers_completed,
            'country_preferences': self.registration.country_preference_ids,
            'committee_preferences':
            list(self.registration.committee_preferences.all()),
            'registration_comments': self.registration.registration_comments,
            'delegate_fees_owed': float(self.registration.delegate_fees_owed),
            'delegate_fees_paid': float(self.registration.delegate_fees_paid),
            'registration_fee_paid': self.registration.registration_fee_paid,
            'assignments_finalized': True,
            'modified_at': self.registration.modified_at.isoformat()
        })


class RegistrationDetailPatchTest(tests.PartialUpdateAPITestCase):
    url_name = 'api:registration_detail'

    def setUp(self):
        self.advisor = models.new_user(username='advisor', password='advisor')
        self.school = models.new_school(user=self.advisor)
        self.registration = models.new_registration(school=self.school)
        self.params = {
            'conference': self.registration.conference.session,
            'school': self.registration.school.id,
            'country_preferences': self.registration.country_preference_ids,
            'assignments_finalized': True
        }

    def test_anonymous_user(self):
        '''Anonymous user should not be able to submit a partial update.'''
        response = self.get_response(self.registration.id, self.params)
        self.assertNotAuthenticated(response)

    def test_other_user(self):
        '''A user should not be able to partially update another user's info.'''
        other_user = models.new_user(username='username', password='password')
        school = models.new_school(user=other_user)
        self.client.login(username='username', password='password')
        response = self.get_response(self.registration.id, self.params)
        self.assertPermissionDenied(response)

    def test_advisor(self):
        '''An advisor should be able to partially update his/her info.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.registration.id, self.params)
        self.assertEqual(response.data, {
            'id': self.registration.id,
            'school': self.registration.school.id,
            'conference': self.registration.conference.session,
            'registered_at': self.registration.registered_at.isoformat(),
            'is_waitlisted': self.registration.is_waitlisted,
            'num_beginner_delegates': self.registration.num_beginner_delegates,
            'num_intermediate_delegates':
            self.registration.num_intermediate_delegates,
            'num_advanced_delegates': self.registration.num_advanced_delegates,
            'num_spanish_speaking_delegates':
            self.registration.num_spanish_speaking_delegates,
            'num_chinese_speaking_delegates':
            self.registration.num_chinese_speaking_delegates,
            'waivers_completed': self.registration.waivers_completed,
            'country_preferences': self.registration.country_preference_ids,
            'committee_preferences':
            list(self.registration.committee_preferences.all()),
            'registration_comments': self.registration.registration_comments,
            'delegate_fees_owed': float(self.registration.delegate_fees_owed),
            'delegate_fees_paid': float(self.registration.delegate_fees_paid),
            'registration_fee_paid': self.registration.registration_fee_paid,
            'assignments_finalized': True,
            'modified_at': self.registration.modified_at.isoformat()
        })

    def test_superuser(self):
        '''A superuser should be able to partially update anyone's info.'''
        models.new_superuser(username='super', password='user')
        self.client.login(username='super', password='user')
        response = self.get_response(self.registration.id, self.params)
        self.assertEqual(response.data, {
            'id': self.registration.id,
            'school': self.registration.school.id,
            'conference': self.registration.conference.session,
            'registered_at': self.registration.registered_at.isoformat(),
            'is_waitlisted': self.registration.is_waitlisted,
            'num_beginner_delegates': self.registration.num_beginner_delegates,
            'num_intermediate_delegates':
            self.registration.num_intermediate_delegates,
            'num_advanced_delegates': self.registration.num_advanced_delegates,
            'num_spanish_speaking_delegates':
            self.registration.num_spanish_speaking_delegates,
            'num_chinese_speaking_delegates':
            self.registration.num_chinese_speaking_delegates,
            'waivers_completed': self.registration.waivers_completed,
            'country_preferences': self.registration.country_preference_ids,
            'committee_preferences':
            list(self.registration.committee_preferences.all()),
            'registration_comments': self.registration.registration_comments,
            'delegate_fees_owed': float(self.registration.delegate_fees_owed),
            'delegate_fees_paid': float(self.registration.delegate_fees_paid),
            'registration_fee_paid': self.registration.registration_fee_paid,
            'assignments_finalized': True,
            'modified_at': self.registration.modified_at.isoformat()
        })


class RegistrationDetailDeleteTest(auto.DestroyAPIAutoTestCase):
    url_name = 'api:registration_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_registration()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_other_user(self):
        other_user = models.new_user()
        school = models.new_school(user=other_user)
        self.as_user(other_user).do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_advisor(self):
        advisor = User.objects.get(school_id=self.object.school_id)
        advisor.PASSWORD_FOR_TESTS_ONLY = 'test'
        self.as_user(advisor).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()
