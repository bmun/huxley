# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import date

from django.db import IntegrityError
from django.test import TestCase

from huxley.core.models import (Assignment, Committee, Conference, Country,
                                CountryPreference, School)
from huxley.utils.test import TestSchools

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

    def test_update_country_preferences(self):
        school = TestSchools.new_school()
        country_ids = [0, 1, 2, 2, 0, 3]
        self.assertEquals(0, CountryPreference.objects.all().count())

        prefs = School.update_country_preferences(school.id, country_ids)
        self.assertEquals([1, 2, 3], prefs)

        self.assertEquals(3, CountryPreference.objects.all().count())
        for i, country_preference in enumerate(CountryPreference.objects.all()):
            self.assertEquals(prefs[i], country_preference.country_id)
            self.assertEquals(school.id, country_preference.school_id)

    def test_update_fees(self):
        '''Fees should be calculated when a School is created/updated.'''
        b, i, a = 3, 5, 7
        school = TestSchools.new_school(
            beginner_delegates=b,
            intermediate_delegates=i,
            advanced_delegates=a,
        )

        self.assertEquals(
            school.fees_owed,
            school.REGISTRATION_FEE + school.DELEGATE_FEE * (b + i + a),
        )

        b2, i2, a2 = 5, 10, 15
        school.beginner_delegates = b2
        school.intermediate_delegates = i2
        school.advanced_delegates = a2
        school.save()

        self.assertEquals(
            school.fees_owed,
            school.REGISTRATION_FEE + school.DELEGATE_FEE * (b2 + i2 + a2),
        )

class AssignmentTest(TestCase):

    def test_uniqueness(self):
        '''Country and committee fields must be unique.'''
        Assignment.objects.create(committee_id=1, country_id=1)
        with self.assertRaises(IntegrityError):
            Assignment.objects.create(committee_id=1, country_id=1)

