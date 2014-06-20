# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import status

from huxley.accounts.models import User
from huxley.api.tests import CreateAPITestCase
from huxley.core.models import School
from huxley.utils.test import TestSchools


class CreateSchoolTestCase(CreateAPITestCase):
    url_name = 'api:school_list'
    params = {'name': 'Berkeley Prep',
            'address': '1 BMUN way',
            'city': 'Oakland',
            'state': 'California',
            'zip_code': 94720,
            'country': 'USA',
            'primary_name': 'Kunal Mehta',
            'primary_gender': 1,
            'primary_email': 'KunalMehta@huxley.org',
            'primary_phone': '(999) 999-9999',
            'primary_type': 2,
            'program_type': User.TYPE_ADVISOR}

    def test_empty_fields(self):
        '''This should not allow for required fields to be empty.'''
        response = self.get_response(params=self.get_params(name='',
                                                            address='',
                                                            city='',
                                                            state='',
                                                            zip_code='',
                                                            country='',
                                                            primary_name='',
                                                            primary_email='',
                                                            primary_phone='',
                                                            program_type=''))
        self.assertEqual(response.data,
            {"city": ["This field is required."],
            "name": ["This field is required."],
            "primary_phone": ["This field is required."],
            "program_type": ["This field is required."],
            "country": ["This field is required."],
            "state": ["This field is required."],
            "primary_name": ["This field is required."],
            "primary_email": ["This field is required."],
            "address": ["This field is required."],
            "zip_code": ["This field is required."]})

    def test_valid(self):
        params = self.get_params()
        response = self.get_response(params)

        school_query = School.objects.filter(id=response.data['id'])
        self.assertTrue(school_query.exists())

        school = School.objects.get(id=response.data['id'])
        self.assertEqual(response.data, {
            'id': school.id,
            'registered': school.registered.isoformat(),
            'name': school.name,
            'address': school.address,
            'city': school.city,
            'state': school.state,
            'zip_code': school.zip_code,
            'country': school.country,
            'primary_name': school.primary_name,
            'primary_gender': school.primary_gender,
            'primary_email': school.primary_email,
            'primary_phone': school.primary_phone,
            'primary_type': school.primary_type,
            'secondary_name': school.secondary_name,
            'secondary_gender': school.secondary_gender,
            'secondary_email': school.secondary_email,
            'secondary_phone': school.secondary_phone,
            'secondary_type': school.secondary_type,
            'program_type': school.program_type,
            'times_attended': school.times_attended,
            'international': school.international,
            'waitlist': school.waitlist,
            'beginner_delegates': school.beginner_delegates,
            'intermediate_delegates': school.intermediate_delegates,
            'advanced_delegates': school.advanced_delegates,
            'spanish_speaking_delegates': school.spanish_speaking_delegates,
            'bilingual': school.bilingual,
            'crisis': school.crisis,
            'small_specialized': school.small_specialized,
            'mid_large_specialized': school.mid_large_specialized,
            'registration_comments': school.registration_comments})

    def test_invalid_state(self):
        '''States should be alphabetical.'''
        params = self.get_params(state='99999')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'state')

    def test_invalid_address(self):
        '''Address should be alphanumerical'''
        params = self.get_params(address='@#/!?')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'address')

    def test_invalid_city(self):
        '''City should be alphabetical.'''
        params = self.get_params(city='99999')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'city')

    def test_invalid_country(self):
        '''Country should be alphabetical.'''
        params = self.get_params(country='99999')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'country')

    def test_invalid_primary_name(self):
        '''Primary name should be alphabetical.'''
        params = self.get_params(primary_name='123@#?$!')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'primary_name')

    def test_invalid_primary_email(self):
        '''Primary email should only have valid email characters.'''
        params = self.get_params(primary_email='####@9999.999')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'primary_email')

    def test_invalid_primary_email_format(self):
        '''Primary email should match email format.'''
        params = self.get_params(primary_email='999999')

        response = self.get_response(params=params)

        self.assertEqual(response.data, {'primary_email': [u'Enter a valid email address.']})

    def test_invalid_US_primary_phone(self):
        '''Primary phone should be numerical.'''
        params = self.get_params(primary_phone='ABC')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'primary_phone')

    def test_invalid_international_primary_phone(self):
        '''Primary phone should be numerical.'''
        params = self.get_params(primary_phone='ABC')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'primary_phone')

    def test_invalid_secondary_name(self):
        '''Secondary name should be alphabetical.'''
        params = self.get_params(secondary_name='@!#$%^?')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'secondary_name')

    def test_invalid_secondary_email(self):
        '''Secondary email should only have valid email characters.'''
        params = self.get_params(secondary_email='####@9999.999')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'secondary_email')

    def test_invalid_primary_email_format(self):
        '''Primary email should match email format.'''
        params = self.get_params(secondary_email='999999')

        response = self.get_response(params=params)

        self.assertEqual(response.data, {'secondary_email': [u'Enter a valid email address.']})

    def test_invalid_US_secondary_phone(self):
        '''Secondary phone should be numerical.'''
        params = self.get_params(secondary_phone='ABC')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'secondary_phone')

    def test_invalid_international_secondary_phone(self):
        '''Secondary_phone phone should be numerical.'''
        params = self.get_params(international=School.LOCATION_INTERNATIONAL,
            secondary_phone='ABC')

        response = self.get_response(params=params)

        self.assertInvalidCharacters(response, 'secondary_phone')

    def test_duplicate_school_name(self):
        '''Validators should not allow for duplicated school names.'''
        params = self.get_params()
        school = TestSchools.new_school(name=params['name'])

        response = self.get_response(params=params)

        self.assertEqual(response.data,
            {"name": ["A school with the name \"%s\" has already been registered." %params['name']]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
