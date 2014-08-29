# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from contextlib import closing
from datetime import date

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.core.models import *
from huxley.utils.test import TestFiles, TestUsers, TestSchools


class ConferenceTest(TestCase):

    def setUp(self):
        self.conference = Conference.objects.create(
            session=61,
            start_date=date(2013, 3, 1),
            end_date=date(2013, 3, 3),
            reg_open=date(2012, 9, 1),
            early_reg_close=date(2013, 1, 10),
            reg_close=date(2013, 2, 28)
        )

    def test_default_fields(self):
        """ Tests that fields with default values are correctly set. """
        self.assertEquals(0, self.conference.min_attendance)
        self.assertEquals(0, self.conference.max_attendance)

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        self.assertTrue(self.conference.__unicode__() == 'BMUN 61')


class CountryTest(TestCase):

    def setUp(self):
        self.country = Country.objects.create(name='Lolville')

    def test_default_fields(self):
        """ Tests that fields with default values are correctly set. """
        self.assertFalse(self.country.special)

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        self.assertTrue(self.country.__unicode__() == 'Lolville')


class CommitteeTest(TestCase):

    def setUp(self):
        self.committee = Committee.objects.create(
            name='DISC',
            full_name='Disarmament and International Security'
        )

    def test_default_fields(self):
        """ Tests that fields with default values are correctly set. """
        self.assertEquals(2, self.committee.delegation_size)
        self.assertFalse(self.committee.special)

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        self.assertEquals('DISC', self.committee.__unicode__())


class SchoolTest(TestCase):

    fixtures = ['countries', 'committees']

    def test_update_country_preferences(self):
        pass

    def test_update_committee_preferences(self):
        pass

    def test_update_delegate_slots(self):
        pass

    def test_get_country_preferences(self):
        pass

    def test_get_delegate_slots(self):
        pass

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        pass


class AssignmentTest(TestCase):

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        pass


class CountryPreferenceTest(TestCase):

    def test_shuffle(self):
        """ Tests that the function correctly shuffles the list and pads it
            to length 10. """
        unshuffled = [1, 2, 3, 4, 5, 6]
        correct = [(1, 6), (2, None), (3, None), (4, None), (5, None)]
        self.assertEquals(correct, CountryPreference.shuffle(unshuffled))

    def test_unshuffle(self):
        """ Tests that the function correctly unshuffles the list. """
        shuffled = [(1, 6), (2, None), (3, None), (4, None), (5, None)]
        correct = [1, 2, 3, 4, 5, 6]
        self.assertEquals(correct, CountryPreference.unshuffle(shuffled))

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        pass


class DelegateSlotTest(TestCase):

    def test_update_or_create_delegate(self):
        pass

    def test_delete_delegate_if_exists(self):
        pass

    def test_update_delegate_attendance(self):
        pass

    def test_properties(self):
        pass

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        pass


class DelegateTest(TestCase):

    def test_properties(self):
        pass

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        pass


class CommitteeAdminTest(TestCase):

    def test_import(self):
        ''' Test that the admin panel can import committees.'''
        TestUsers.new_superuser(username='testuser', password='test')
        self.client.login(username='testuser', password='test')

        f = TestFiles.new_csv([
            ['SPD', 'Special Pôlitical and Decolonization', 2, ''],
            ['USS', 'United States Senate', 2, True]
        ])

        with closing(f) as f:
            self.client.post(reverse('admin:core_committee_load'), {'csv': f})

        self.assertTrue(Committee.objects.filter(
            name='SPD',
            full_name='Special Pôlitical and Decolonization',
            delegation_size=2,
            special=False
        ).exists())
        self.assertTrue(Committee.objects.filter(
            name='USS',
            full_name='United States Senate',
            delegation_size=2,
            special=True
        ).exists())


class CountryAdminTest(TestCase):

    def test_import(self):
        ''' Test that the admin panel can import countries. '''
        TestUsers.new_superuser(username='testuser', password='test')
        self.client.login(username='testuser', password='test')

        f = TestFiles.new_csv([
            ['United States of America', ''],
            ['Barbara Boxer', True],
            ["Côte d'Ivoire", '']
        ])

        with closing(f) as f:
            self.client.post(reverse('admin:core_country_load'), {'csv': f})

        self.assertTrue(Country.objects.filter(
            name='United States of America',
            special=False
        ).exists())
        self.assertTrue(Country.objects.filter(
            name='Barbara Boxer',
            special=True
        ).exists())
        self.assertTrue(Country.objects.filter(
            name="Côte d'Ivoire",
            special=False
        ).exists())


class SchoolAdminTest(TestCase):

    def test_info_export(self):
        '''Test that the admin panel can properly export a list of schools.'''
        TestUsers.new_user(username='testuser1', password='test1')
        TestUsers.new_superuser(username='testuser2', password='test2')
        self.client.login(username='testuser1', password='test1')
        school = TestSchools.new_school()
        self.client.logout()
        self.client.login(username='testuser2', password='test2')

        response = self.client.get(reverse('admin:core_school_info'))

        self.assertTrue(response)

        header = [
            "Name",
            "Address",
            "City",
            "State",
            "Zip Code",
            "Country",
            "Primary Name",
            "Primary Gender",
            "Primary Email",
            "Primary Phone",
            "Primary Type",
            "Secondary Name",
            "Secondary Gender",
            "Secondary Email",
            "Secondary Phone",
            "Secondary Type",
            "Program Type",
            "Times Attended",
            "International",
            "Waitlist",
            "Beginners",
            "Intermediates",
            "Advanced",
            "Spanish Speakers",
            "Bilingual?",
            "Crisis?",
            "Small Specialized?",
            "Mid-Large Specialized?",
            "Registration Comments",
            "Registration Fee",
            "Registration Fee Paid",
            "Registration Fee Balance",
            "Delegation Fee",
            "Delegation Fee Paid",
            "Delegation Fee Balance"
            ]

        fields_csv = ",".join(map(str, header)) + "\r\n"

        fields = [school.name,
                school.address,
                school.city,
                school.state,
                school.zip_code,
                school.country,
                school.primary_name,
                school.primary_gender,
                school.primary_email,
                school.primary_phone,
                school.primary_type,
                school.secondary_name,
                school.secondary_gender,
                school.secondary_email,
                school.secondary_phone,
                school.secondary_type,
                school.program_type,
                school.times_attended,
                school.international,
                school.waitlist,
                school.beginner_delegates,
                school.intermediate_delegates,
                school.advanced_delegates,
                school.spanish_speaking_delegates,
                school.prefers_bilingual,
                school.prefers_crisis,
                school.prefers_small_specialized,
                school.prefers_mid_large_specialized,
                school.registration_comments,
                school.registration_fee,
                school.registration_fee_paid,
                school.registration_fee_balance,
                school.delegation_fee,
                school.delegation_fee_paid,
                school.delegation_fee_balance]

        fields_csv += ",".join(map(str, fields))
        self.assertEquals(fields_csv, response.content[:-2])

    def test_preference_export(self):
        '''Test that the admin panel can properly export school preferences.'''
        TestUsers.new_user(username='testuser1', password='test1')
        TestUsers.new_superuser(username='testuser2', password='test2')
        self.client.login(username='testuser1', password='test1')
        school = TestSchools.new_school()
        self.client.logout()
        self.client.login(username='testuser2', password='test2')

        response = self.client.get(reverse('admin:core_school_preferences'))

        self.assertTrue(response)

        header = [
            "Name",
            "Assignments Requested",
            "Beginners",
            "Intermediates",
            "Advanced",
            "Spanish Speakers",
            "Bilingual?",
            "Crisis?",
            "Small Specialized?",
            "Mid-Large Specialized?",
            "Country 1",
            "Country 2",
            "Country 3",
            "Country 4",
            "Country 5",
            "Country 6",
            "Country 7",
            "Country 8",
            "Country 9",
            "Country 10",
            "Registration Comments"
            ]

        fields_csv = ",".join(map(str, header)) + "\r\n"

        countryprefs = [c for c in school.countrypreferences.all()]
        countryprefs += [''] * (10 - len(countryprefs))

        fields = [
                school.name,
                school.beginner_delegates + school.intermediate_delegates + school.advanced_delegates,
                school.beginner_delegates,
                school.intermediate_delegates,
                school.advanced_delegates,
                school.spanish_speaking_delegates,
                school.prefers_bilingual,
                school.prefers_crisis,
                school.prefers_small_specialized,
                school.prefers_mid_large_specialized]
        fields.extend(countryprefs)
        fields.append(school.registration_comments)

        fields_csv += ",".join(map(str, fields))
        self.assertEquals(fields_csv, response.content[:-2])
