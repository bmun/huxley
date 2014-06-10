# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.test import TestCase

from huxley.accounts.forms.registration import RegistrationForm
from huxley.accounts.models import User
from huxley.core.models import *

import re


class RegistrationTest(TestCase):

    fixtures = ['countries.json', 'committees.json']

    valid_params = {'first_name': 'Taeyeon',
                    'last_name': 'Kim',
                    'username': 'taengoo',
                    'password': 'girlsgeneration',
                    'password2': 'girlsgeneration',
                    'school_location': School.LOCATION_USA,
                    'school_name': 'SNSD',
                    'school_address': '123 SNSD Way',
                    'school_city': 'Seoul',
                    'school_state': 'Seoul',
                    'school_zip':12345,
                    'program_type': School.TYPE_CLUB,
                    'times_attended':9,
                    'delegation_size': 9,
                    'primary_name':'Manager',
                    'primary_email':'kimtaeyon@snsd.com',
                    'primary_phone':'(123) 435-7543',
                    'country_pref1': 1,
                    'country_pref2': 2,
                    'country_pref3': 3,
                    'country_pref4': 4,
                    'country_pref5': 5,
                    'country_pref6': 6,
                    'country_pref7': 7,
                    'country_pref8': 8,
                    'country_pref9': 9,
                    'country_pref10': 10}

    def test_sanity(self):
        """ Make sure a form with all valid data works. """
        params = self.valid_params.copy()

        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_required(self):
        """ Make sure all fields except for the optional ones are present
            in the parameters. """
        params = {'first_name':'', 'school_location': School.LOCATION_USA} # Empty string is not valid
        form = RegistrationForm(params)

        valid = form.is_valid()
        self.assertFalse(valid)

        for name, field in form.fields.items():
            if field.required and name != 'school_location':
                self.assertIn(name, form.errors)
            elif name == 'school_state':
                # State is only required if the school is in the US
                self.assertIn('school_state', form.errors)
            else:
                self.assertNotIn(name, form.errors)


    def test_username_length(self):
        """ Tests for minimum username length. """

        # Too short (len: 3)
        params = self.valid_params.copy()
        params['username'] = 'abc' # Too short, so invalid

        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('username', form.errors)
        # Make sure it's the only error (i.e. no other validation errors for usernames)
        self.assertItemsEqual(form.errors['username'], ['Ensure this value has at least 4 characters (it has 3).'])

        # Valid username, since it's at least 4 characters long
        params['username'] = 'abcd'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Valid username, since it's at least 4 characters long
        params['username'] = 'abcdesdfdsfasdf'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_username_chars(self):
        """ Tests for: valid characters (alphanumeric, hyphens, underscores) """

        # All invalid characters
        params = self.valid_params.copy()
        params['username'] = '!@#$'
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('username', form.errors)
        self.assertItemsEqual(form.errors['username'], ['Usernames must be alphanumeric, underscores, and/or hyphens only.'])

        # Mixture of valid and invalid characters
        params['username'] = 'abc!defgh'
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('username', form.errors)
        self.assertItemsEqual(form.errors['username'], ['Usernames must be alphanumeric, underscores, and/or hyphens only.'])

        # Looks valid but isn't
        params['username'] = 'Rick Astley'
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('username', form.errors)
        self.assertItemsEqual(form.errors['username'], ['Usernames must be alphanumeric, underscores, and/or hyphens only.'])

        # Just valid characters
        params['username'] = 'RickAstley'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_create_user(self):
        """ Tests parameters and db insertion """

        params = self.valid_params.copy()
        params['username'] = 'ajummaTaeng'
        form = RegistrationForm(params)

        self.assertTrue(form.is_valid())
        user = form.create_user()

        # Check return value
        self.assertEqual(user.username, params['username'])
        self.assertEqual(user.first_name, params['first_name'])
        self.assertEqual(user.last_name, params['last_name'])

        # Check to see that it's in the database as well
        self.assertTrue(User.objects.filter(id=user.id).exists())


    def test_username_unique(self):
        """ Tests for: uniqueness """

        params = self.valid_params.copy()
        params['username'] = 'abcdef'

        # This should be valid, as 'abcdef' should be unique
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())
        form.create_user()

        # Try again and it should throw a validation error
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('username', form.errors)
        self.assertItemsEqual(form.errors['username'], ['Username \'%s\' is already in use. Please choose another one.' % (params['username'])])


    def test_password_len(self):
        """ Tests for: minimum length """
        params = self.valid_params.copy()
        # Tests len < 6
        params['password'] = 'abcde'
        params['password2'] = 'abcde'

        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('password', form.errors)
        self.assertItemsEqual(form.errors['password'], ['Ensure this value has at least 6 characters (it has 5).'])

        # Tests len == 6
        params['password'] = 'abcdef'
        params['password2'] = 'abcdef'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Tests len > 6
        params['password'] = 'abcdefgh'
        params['password2'] = 'abcdefgh'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_password_confirm(self):
        """ Tests that password and password2 match """

        params = self.valid_params.copy()
        params['password'] = 'abcdef'
        params['password2'] = 'abcdefg'

        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 2)
        self.assertIn('password', form.errors)
        self.assertIn('password2', form.errors)
        self.assertItemsEqual(form.errors['password'], ['Passwords do not match!'])
        self.assertItemsEqual(form.errors['password2'], ['Passwords do not match!'])


    def test_password_chars(self):
        """ Tests that password contains only valid characters (alphanumeric, underscore, ., symbols on number keys) """
        # Invalid characters
        params = self.valid_params.copy()
        params['password'] = '~[]\[]]\[]\[\]'
        params['password2'] = '~[]\[]]\[]\[\]'

        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('password', form.errors)
        self.assertItemsEqual(form.errors['password'], ['Password contains invalid characters.'])

        # Valid characters
        params['password'] = 'abcdefg!@#$%^&*'
        params['password2'] = 'abcdefg!@#$%^&*'

        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_create_school(self):
        """ Tests that the form creates a school object in the DB properly """

        # Test that American schools are created properly
        params = self.valid_params.copy()
        params['school_name'] = 'GirlsGeneration'

        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        school = form.create_school()
        self.assertFalse(school is None)

        self.assertEqual(school.name, params['school_name'])
        self.assertEqual(school.address, params['school_address'])
        self.assertEqual(school.city, params['school_city'])
        self.assertEqual(school.state, params['school_state'])
        self.assertEqual(school.zip_code, str(params['school_zip']))
        self.assertEqual(school.primary_name, params['primary_name'])
        self.assertEqual(school.primary_email, params['primary_email'])
        self.assertEqual(school.primary_phone, params['primary_phone'])
        self.assertEqual(school.program_type, params['program_type'])
        self.assertEqual(school.times_attended, params['times_attended'])
        self.assertEqual(school.delegation_size, params['delegation_size'])
        self.assertFalse(school.international)

        # Make sure state isn't an empty string, or a string of spaces
        # Bit unnecessary though
        matches = re.match('^\s*$', school.state)
        self.assertTrue(matches is None)

        if 'secondary_name' in params:
            self.assertEqual(school.secondary_name, params['secondary_name'])
        if 'secondary_email' in params:
            self.assertEqual(school.secondary_email, params['secondary_email'])
        if 'secondary_phone' in params:
            self.assertEqual(school.secondary_phone, params['secondary_phone'])

        # Check to see that it's in the database as well
        schools_in_db = School.objects.filter(name=params['school_name'])
        self.assertGreater(len(schools_in_db), 0)
        self.assertEqual(schools_in_db[0], school)

        # Test international school creation
        params['school_name'] = 'GirlsGenerationInternational'
        params['school_country'] = '10'
        params['school_location'] = School.LOCATION_INTERNATIONAL
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        school = form.create_school()
        self.assertFalse(school is None)
        self.assertEqual(school.name, params['school_name'])
        self.assertEqual(school.address, params['school_address'])
        self.assertEqual(school.city, params['school_city'])
        self.assertEqual(school.zip_code, str(params['school_zip']))
        self.assertEqual(school.country, params['school_country'])
        self.assertEqual(school.primary_name, params['primary_name'])
        self.assertEqual(school.primary_email, params['primary_email'])
        self.assertEqual(school.primary_phone, params['primary_phone'])
        self.assertEqual(school.program_type, params['program_type'])
        self.assertEqual(school.times_attended, params['times_attended'])
        self.assertEqual(school.delegation_size, params['delegation_size'])
        self.assertTrue(school.international)

        if 'school_state' in params:
            self.assertEqual(school.state, params['school_state'])
        if 'secondary_name' in params:
            self.assertEqual(school.secondary_name, params['secondary_name'])
        if 'secondary_email' in params:
            self.assertEqual(school.secondary_email, params['secondary_email'])
        if 'secondary_phone' in params:
            self.assertEqual(school.secondary_phone, params['secondary_phone'])

        # Check to see that it's in the database as well
        schools_in_db = School.objects.filter(name=params['school_name'])
        self.assertGreater(len(schools_in_db), 0)
        self.assertEqual(schools_in_db[0], school)


    def test_school_uniqueness(self):
        """ Tests that the school name checks if it's unique """
        params = self.valid_params.copy()
        params['school_name'] = 'MySchool'

        # This should be valid, as 'abcdef' should be unique
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())
        form.create_school()

        # This shouldn't be valid.
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('school_name', form.errors)
        self.assertItemsEqual(form.errors['school_name'], ['A school with the name "%s" has already been registered.' % (params['school_name'])])

        # Now try another valid one
        params['school_name'] = 'MySchool2'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_add_country_preferences(self):
        """ Tests that adding country preferences works """
        # Initialization
        params = self.valid_params.copy()
        for i in xrange(1,11):
            params['country_pref' + str(i)] = 0

        # No preferences at all
        params['school_name'] = 'CountryTest1'
        form = RegistrationForm(params)

        self.assertTrue(form.is_valid())
        school = form.create_school()
        self.assertTrue(form.add_country_preferences(school))

        prefs = CountryPreference.objects.filter(school=school)
        self.assertEqual(len(prefs), 0)

        # Couple of random preferences scattered around
        params['school_name'] = 'CountryTest2'
        params['country_pref1'] = 2
        params['country_pref3'] = 10
        params['country_pref7'] = 7
        form = RegistrationForm(params)

        self.assertTrue(form.is_valid())
        school = form.create_school()
        self.assertTrue(form.add_country_preferences(school))

        prefs = CountryPreference.objects.filter(school=school)
        self.assertEqual(len(prefs), 3)

        self.assertEqual(prefs[0].country.id, params['country_pref1'])
        self.assertEqual(prefs[1].country.id, params['country_pref3'])
        self.assertEqual(prefs[2].country.id, params['country_pref7'])


    def test_country_preferences(self):
        """ Tests that country preferences are optional """
        # Initialization
        params = self.valid_params.copy()
        for i in xrange(1,11):
            params['country_pref' + str(i)] = 0

        # Should be valid even with no country preferences
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Couple of unique country preferences; valid
        params['country_pref1'] = 1
        params['country_pref3'] = 10
        params['country_pref7'] = 7

        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_add_committee_preferences(self):
        """ Tests that adding committee preferences works """
        params = self.valid_params.copy()
        params['school_name'] = 'CommitteeTest1'
        form = RegistrationForm(params)

        # No committee preferences
        self.assertTrue(form.is_valid())
        school = form.create_school()
        self.assertTrue(form.add_committee_preferences(school))
        self.assertEqual(len(school.committeepreferences.all()), 0)

        # Some preferences
        params['committee_prefs'] = [13, 14, 19]
        params['school_name'] = 'CommitteeTest2'
        form = RegistrationForm(params)

        self.assertTrue(form.is_valid())
        school = form.create_school()
        self.assertTrue(form.add_committee_preferences(school))
        self.assertEqual(len(school.committeepreferences.all()), 3)

        for committee in school.committeepreferences.all():
            self.assertIn(committee.id, params['committee_prefs'])


    def test_us_phone_nums(self):
        """ Tests the US phone number validation code """
        params = self.valid_params.copy()
        params['school_location'] = School.LOCATION_USA

        # (XXX) XXX-XXXX
        params['primary_phone'] = '(123) 456-7890'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # (XXX) XXX-XXXX xXXXX (extension)
        params['primary_phone'] = '(123) 456-7890 x1234'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # 123-456-7890 (invalid)
        params['primary_phone'] = '123-456-7890'
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('primary_phone', form.errors)
        self.assertItemsEqual(form.errors['primary_phone'], ['Phone in incorrect format.'])

        # (123) 12a-1231 (invalid)
        params['primary_phone'] = '(123) 12a-1231'
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('primary_phone', form.errors)
        self.assertItemsEqual(form.errors['primary_phone'], ['Phone in incorrect format.'])


    def test_international_phone_nums(self):
        """ Tests the international phone number validation code """
        params = self.valid_params.copy()
        params['school_location'] = School.LOCATION_INTERNATIONAL
        params['school_country'] = 'Japan'

        # 1234534653465 (just numbers; valid)
        params['primary_phone'] = '123434645657'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # 1-123-123-1234 (dashes; valid)
        params['primary_phone'] = '1-123-123-1234'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # US format (valid)
        params['primary_phone'] = '(123) 456-7890'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # US format with invalid characters
        params['primary_phone'] = '(12a) 456-7890'
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('primary_phone', form.errors)
        self.assertItemsEqual(form.errors['primary_phone'], ['Phone in incorrect format.'])

        # Numbers with invalid characters
        params['primary_phone'] = '1-234-4a3-as,f'
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('primary_phone', form.errors)
        self.assertItemsEqual(form.errors['primary_phone'], ['Phone in incorrect format.'])


    def test_school_country(self):
        """ Tests that school country is filled out when it's an international school """
        params = self.valid_params.copy()

        # Try US first (no country specified)
        params['school_location'] = School.LOCATION_USA
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Try US with a country (shouldn't matter)
        params['school_country'] = 'America'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Try international (with no country specified)
        params = self.valid_params.copy()
        params['school_location'] = School.LOCATION_INTERNATIONAL
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn('school_country', form.errors)
        self.assertItemsEqual(form.errors['school_country'], ['International schools must provide a country.'])

        # Try international (with a country)
        params['school_country'] = 'Japan'
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

