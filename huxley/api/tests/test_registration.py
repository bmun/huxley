# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api.tests import CreateAPITestCase
from huxley.core.models import Conference, Registration
from huxley.utils.test import models


class RegistrationListPostTest(CreateAPITestCase):

    fixtures = ['conference']

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
            'fees_owed': float(registration.fees_owed),
            'fees_paid': float(registration.fees_paid),
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
        fees_owed = response.data['fees_owed']
        fees_paid = response.data['fees_paid']

        self.assertEqual(fees_owed, float(registration.fees_owed))
        self.assertEqual(fees_paid, float(registration.fees_paid))
        self.assertNotEqual(fees_owed, 2000.0)
        self.assertNotEqual(fees_paid, 2000.0)

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

    def test_delegate_total(self):
        '''Validator shouldn't let there be more spanish or chinese speaking
		   delegates than there are total delegates.'''
        school = models.new_school()
        conference = Conference.get_current()
        params = self.get_params(
            school=school.id,
            conference=conference.session,
            num_beginner_delegates=1,
            num_intermediate_delegates=1,
            num_advanced_delegates=1,
            num_spanish_speaking_delegates=4,
            num_chinese_speaking_delegates=4)

        response = self.get_response(params=params)
        self.assertEqual(response.data,
                         {'num_spanish_speaking_delegates':
                          [u'Cannot exceed total number of delegates.'],
                          'num_chinese_speaking_delegates':
                          [u'Cannot exceed total number of delegates.']})
