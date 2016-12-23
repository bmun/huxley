# -*- coding: utf-8 -*-
# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from huxley.core.models import (Assignment, Committee, Conference, Country,
                                CountryPreference, Delegate)
from huxley.utils.test import (TestAssignments, TestCommittees, TestCountries,
                               TestDelegates, TestSchools)


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

    fixtures = ['conference']

    def test_update_country_preferences(self):
        '''It should filter and replace the school's country preferences.'''
        s1 = TestSchools.new_school()
        s2 = TestSchools.new_school()
        c1 = TestCountries.new_country().id
        c2 = TestCountries.new_country().id
        c3 = TestCountries.new_country().id

        country_ids = [0, c1, c2, c2, 0, c3]
        self.assertEquals(0, CountryPreference.objects.all().count())

        s1.update_country_preferences(country_ids)
        self.assertEquals([c1, c2, c3], s1.country_preference_ids)

        s2.update_country_preferences(country_ids)
        self.assertEquals([c1, c2, c3], s2.country_preference_ids)

        s1.update_country_preferences([c3, c1])
        self.assertEquals([c3, c1], s1.country_preference_ids)
        self.assertEquals([c1, c2, c3], s2.country_preference_ids)

    def test_update_fees(self):
        '''Fees should be calculated when a School is created/updated.'''
        b, i, a = 3, 5, 7
        school = TestSchools.new_school(
            beginner_delegates=b,
            intermediate_delegates=i,
            advanced_delegates=a,
        )

        conference = Conference.get_current()
        registration_fee = conference.registration_fee
        delegate_fee = conference.delegate_fee

        self.assertEquals(
            school.fees_owed, registration_fee + delegate_fee * (b + i + a),
        )

        b2, i2, a2 = 5, 10, 15
        school.beginner_delegates = b2
        school.intermediate_delegates = i2
        school.advanced_delegates = a2
        school.save()

        self.assertEquals(
            school.fees_owed, registration_fee + delegate_fee * (b2 + i2 + a2),
        )

    def test_update_waitlist(self):
        '''New schools should be waitlisted based on the conference waitlist field.'''
        s1 = TestSchools.new_school()
        self.assertFalse(s1.waitlist)

        conference = Conference.get_current()
        conference.waitlist_reg = True
        conference.save()

        s1.save()
        self.assertFalse(s1.waitlist)
        s2 = TestSchools.new_school()
        self.assertTrue(s2.waitlist)


class AssignmentTest(TestCase):

    fixtures = ['conference']

    def test_uniqueness(self):
        '''Country and committee fields must be unique.'''
        Assignment.objects.create(committee_id=1, country_id=1)
        with self.assertRaises(IntegrityError):
            Assignment.objects.create(committee_id=1, country_id=1)

    def test_update_assignments(self):
        '''It should correctly update the set of country assignments.'''
        cm1 = TestCommittees.new_committee(name='CM1')
        cm2 = TestCommittees.new_committee(name='CM2')
        ct1 = TestCountries.new_country(name='CT1')
        ct2 = TestCountries.new_country(name='CT2')
        ct3 = TestCountries.new_country(name='CT3')
        s1 = TestSchools.new_school(name='S1')
        s2 = TestSchools.new_school(name='S2')

        Assignment.objects.bulk_create([
            Assignment(committee_id=cm.id, country_id=ct.id, school_id=s1.id)
            for ct in [ct1, ct2]
            for cm in [cm1, cm2]
        ])

        a = Assignment.objects.get(committee_id=cm2.id, country_id=ct2.id)
        d1 = TestDelegates.new_delegate(school=s1, assignment=a)
        d2 = TestDelegates.new_delegate(school=s1, assignment=a)

        # TODO: Also assert on delegate deletion.
        updates = [
            (cm1, ct1, s1, False),
            (cm1, ct2, s1, False),
            (cm1, ct3, s1, False),   # ADDED
            # (cm2, ct1, s1), # DELETED
            (cm2, ct2, s2, False),   # UPDATED
            (cm2, ct3, s2, False),   # ADDED
        ]

        Assignment.update_assignments(updates)
        new_assignments = [a[1:] for a in Assignment.objects.all().values_list()]
        delegates = Delegate.objects.all()
        updates = [(cm.id, ct.id, s.id, rej) for cm, ct, s, rej in updates]
        self.assertEquals(set(updates), set(new_assignments))
        self.assertEquals(len(delegates), 2)

    def test_update_assignment(self):
        '''Tests that when an assignment changes schools, its rejected
           field is set to False and any delegates assigned to it are
           no longer assigned to it.'''
        s1 = TestSchools.new_school(name='S1')
        s2 = TestSchools.new_school(name='S2')
        a = TestAssignments.new_assignment(school=s1, rejected=True)
        d1 = TestDelegates.new_delegate(school=s1, assignment=a)
        d2 = TestDelegates.new_delegate(school=s1, assignment=a)
        self.assertEquals(a.delegates.count(), 2)
        self.assertTrue(a.rejected)

        a.school = s2
        a.save()

        self.assertEquals(a.delegates.count(), 0)
        self.assertEquals(a.rejected, False)

class CountryPreferenceTest(TestCase):

    def test_uniqueness(self):
        '''Country and school fields should be unique.'''
        CountryPreference.objects.create(school_id=1, country_id=1, rank=1)
        with self.assertRaises(IntegrityError):
            CountryPreference.objects.create(school_id=1, country_id=1, rank=1)

class DelegateTest(TestCase):

    fixtures = ['conference']

    def test_save(self):
        """
        A delegate's school field and a delegate's assignment's school field
        should be the same if they both exist on the delegate.
        """
        school = TestSchools.new_school(name='S1')
        assignment = TestAssignments.new_assignment()

        self.assertRaises(ValidationError, Delegate.objects.create,
            name="Test Delegate",
            school=school,
            assignment=assignment
        )
