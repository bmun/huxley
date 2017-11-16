# -*- coding: utf-8 -*-
# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from huxley.core.models import (Assignment, Committee, Conference, Country,
                                CountryPreference, Delegate)
from huxley.utils.test import models


class ConferenceTest(TestCase):
    def setUp(self):
        self.conference = Conference.objects.create(
            session=61,
            start_date=date(2013, 3, 1),
            end_date=date(2013, 3, 3),
            reg_open=date(2012, 9, 1),
            early_reg_close=date(2013, 1, 10),
            reg_close=date(2013, 2, 28))

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
            name='DISC', full_name='Disarmament and International Security')

    def test_default_fields(self):
        """ Tests that fields with default values are correctly set. """
        self.assertEquals(2, self.committee.delegation_size)
        self.assertFalse(self.committee.special)

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        self.assertEquals('DISC', self.committee.__unicode__())


class AssignmentTest(TestCase):

    fixtures = ['conference']

    def test_uniqueness(self):
        '''Country and committee fields must be unique.'''
        Assignment.objects.create(committee_id=1, country_id=1)
        with self.assertRaises(IntegrityError):
            Assignment.objects.create(committee_id=1, country_id=1)

    def test_update_assignments(self):
        '''It should correctly update the set of country assignments.'''
        cm1 = models.new_committee(name='CM1')
        cm2 = models.new_committee(name='CM2')
        ct1 = models.new_country(name='CT1')
        ct2 = models.new_country(name='CT2')
        ct3 = models.new_country(name='CT3')
        s1 = models.new_school(name='S1')
        r1 = models.new_registration(school=s1)
        s2 = models.new_school(name='S2')
        r2 = models.new_registration(school=s2)

        Assignment.objects.bulk_create([
            Assignment(
                committee_id=cm.id, country_id=ct.id, registration_id=r1.id)
            for ct in [ct1, ct2] for cm in [cm1, cm2]
        ])

        a = Assignment.objects.get(committee_id=cm2.id, country_id=ct2.id)
        d1 = models.new_delegate(school=s1, assignment=a)
        d2 = models.new_delegate(school=s1, assignment=a)

        # TODO: Also assert on delegate deletion.
        updates = [
            (cm1, ct1, s1, False),
            (cm1, ct2, s1, False),
            (cm1, ct3, s1, False),  # ADDED
            # (cm2, ct1, s1), # DELETED
            (cm2, ct2, s2, False),  # UPDATED
            (cm2, ct3, s2, False),  # ADDED
        ]

        all_assignments = [
            (cm1.id, ct1.id, r1.id, False),
            (cm1.id, ct2.id, r1.id, False),
            (cm1.id, ct3.id, r1.id, False),
            (cm2.id, ct2.id, r2.id, False),
            (cm2.id, ct3.id, r2.id, False),
            (cm2.id, ct1.id, r1.id, False),
        ]

        Assignment.update_assignments(updates)
        assignments = [a[1:] for a in Assignment.objects.all().values_list()]
        delegates = Delegate.objects.all()
        self.assertEquals(set(all_assignments), set(assignments))
        self.assertEquals(len(delegates), 2)

    def test_update_assignment(self):
        '''Tests that when an assignment changes schools, its rejected
           field is set to False and any delegates assigned to it are
           no longer assigned to it.'''
        s1 = models.new_school(name='S1')
        r1 = models.new_registration(school=s1)
        s2 = models.new_school(name='S2')
        r2 = models.new_registration(school=s2)
        a = models.new_assignment(registration=r1, rejected=True)
        d1 = models.new_delegate(school=s1, assignment=a)
        d2 = models.new_delegate(school=s1, assignment=a)
        self.assertEquals(a.delegates.count(), 2)
        self.assertTrue(a.rejected)

        a.registration = r2
        a.save()

        self.assertEquals(a.delegates.count(), 0)
        self.assertEquals(a.rejected, False)


class CountryPreferenceTest(TestCase):
    def test_uniqueness(self):
        '''Country and school fields should be unique.'''
        CountryPreference.objects.create(
            registration_id=1, country_id=1, rank=1)
        with self.assertRaises(IntegrityError):
            CountryPreference.objects.create(
                registration_id=1, country_id=1, rank=1)


class DelegateTest(TestCase):

    fixtures = ['conference']

    def test_save(self):
        """
        A delegate's school field and a delegate's assignment's school field
        should be the same if they both exist on the delegate.
        """
        school = models.new_school(name='S1')
        registration = models.new_registration()
        assignment = models.new_assignment(registration=registration)

        self.assertRaises(
            ValidationError,
            Delegate.objects.create,
            name="Test Delegate",
            school=school,
            assignment=assignment)


class RegistrationTest(TestCase):

    fixtures = ['conference']

    def test_uniqueness(self):
        '''Is defined uniquely by its school and conference.'''
        s = models.new_school()
        c = Conference.get_current()
        r1 = models.new_registration(school=s, conference=c)
        with self.assertRaises(IntegrityError):
            r2 = models.new_registration(school=s, conference=c)

    def test_update_fees(self):
        '''Fees should be calculated when a Registration is created/updated.'''
        b, i, a = 3, 5, 7
        registration = models.new_registration(
            num_beginner_delegates=b,
            num_intermediate_delegates=i,
            num_advanced_delegates=a, )

        conference = Conference.get_current()
        delegate_fee = conference.delegate_fee

        self.assertEquals(registration.delegate_fees_owed,
                          delegate_fee * (b + i + a), )

        b2, i2, a2 = 5, 10, 15
        registration.num_beginner_delegates = b2
        registration.num_intermediate_delegates = i2
        registration.num_advanced_delegates = a2
        registration.save()

        self.assertEquals(registration.delegate_fees_owed,
                          delegate_fee * (b2 + i2 + a2), )

    def test_update_waitlist(self):
        '''New registrations should be waitlisted based on the conference waitlist field.'''
        r1 = models.new_registration()
        self.assertFalse(r1.is_waitlisted)

        conference = Conference.get_current()
        conference.waitlist_reg = True
        conference.save()

        r1.save()
        self.assertFalse(r1.is_waitlisted)
        r2 = models.new_registration()
        self.assertTrue(r2.is_waitlisted)

    def test_update_country_preferences(self):
        '''It should filter and replace the country preferences.'''
        r1 = models.new_registration()
        r2 = models.new_registration()
        c1 = models.new_country().id
        c2 = models.new_country().id
        c3 = models.new_country().id

        country_ids = [0, c1, c2, c2, 0, c3]
        self.assertEquals(0, CountryPreference.objects.all().count())

        r1.update_country_preferences(country_ids)
        self.assertEquals([c1, c2, c3], r1.country_preference_ids)

        r2.update_country_preferences(country_ids)
        self.assertEquals([c1, c2, c3], r2.country_preference_ids)

        r1.update_country_preferences([c3, c1])
        self.assertEquals([c3, c1], r1.country_preference_ids)
        self.assertEquals([c1, c2, c3], r2.country_preference_ids)


class PositionPaperTest(TestCase):
    def setup(self):
        self.position_paper = PositionPaper()

    def test_default_values(self):
        self.assertEquals(self.position_paper.score_1, 0)
        self.assertEquals(self.position_paper.score_2, 0)
        self.assertEquals(self.position_paper.score_3, 0)
        self.assertEquals(self.position_paper.score_4, 0)
        self.assertEquals(self.position_paper.score_5, 0)
        self.assertFalse(self.position_paper.graded)

    def test_unicode(self):
        self.assertEquals(str(self.position_paper.id), self.position_paper.__unicode__())
        

class RubricTest(TestCase):
    def setup(self):
        self.rubric = Rubric()

    def test_default_values(self):
        self.assertEquals(self.rubric.grade_category_1, '')
        self.assertEquals(self.rubric.grade_category_2, '')
        self.assertEquals(self.rubric.grade_category_3, '')
        self.assertEquals(self.rubric.grade_category_4, '')
        self.assertEquals(self.rubric.grade_category_5, '')

        self.assertEquals(self.rubric.grade_value_1, 10)
        self.assertEquals(self.rubric.grade_value_2, 10)
        self.assertEquals(self.rubric.grade_value_3, 10)
        self.assertEquals(self.rubric.grade_value_4, 10)
        self.assertEquals(self.rubric.grade_value_5, 10)

    def test_unicode(self):
        self.assertEquals(str(self.rubric.id), self.rubric.__unicode__())
