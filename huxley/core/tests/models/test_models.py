# -*- coding: utf-8 -*-
# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from huxley.core.models import (
    Assignment, Committee, CommitteeFeedback, Conference, Country,
    CountryPreference, Delegate, PositionPaper, Room, RoomComment, Rubric, SecretariatMember)

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
    """ONLY EDIT TEST_UNIQUE METHOD"""
    def setUp(self):
        self.room_1 = Room.objects.create(building_name='Dwinelle', 
                                          room_number=55, 
                                          number_of_seats=200)

        self.room_2 = Room.objects.create(building_name='Dwinelle', 
                                          room_number=56, 
                                          number_of_seats=200)

        self.room_3 = Room.objects.create(building_name='Dwinelle', 
                                          room_number=57, 
                                          number_of_seats=200)

        self.committee = Committee.objects.create(
            name='DISC', 
            full_name='Disarmament and International Security', 
            room_day_one=self.room_1,
            room_day_two=self.room_2,
            room_day_three=self.room_3)

        self.committee_2 = Committee.objects.create(
            name='ICJ', 
            full_name='International Court of Justice')

    def test_unique(self):
        """Tests that two committees cannot have the same room on the same day."""
        self.assertRaises(
            ValidationError,
            Committee.objects.create,
            name='JCC',
            full_name='Joint Cabinet Crisis',
            room_day_one=self.room_1)

        self.assertRaises(
            ValidationError,
            Committee.objects.create,
            name='JCC',
            full_name='Joint Cabinet Crisis',
            room_day_two=self.room_2)

        self.assertRaises(
            ValidationError,
            Committee.objects.create,
            name='JCC',
            full_name='Joint Cabinet Crisis',
            room_day_three=self.room_3)

    def test_default_fields(self):
        """ Tests that fields with default values are correctly set. """
        self.assertEquals(2, self.committee.delegation_size)
        self.assertFalse(self.committee.special)

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        self.assertEquals('DISC', self.committee.__unicode__())

    def test_room_assignment(self):
        """Tests that rooms are assigned correctly."""
        self.assertEquals(self.room_1.id, self.committee.room_day_one.id)
        self.assertEquals(self.room_2.id, self.committee.room_day_two.id)
        self.assertEquals(self.room_3.id, self.committee.room_day_three.id)

    def test_create_rubric(self):
        '''Tests that a committee creates a new rubric upon being
           saved for the first time, but not on subsequent saves.'''
        c = Committee(
            name='DISC', full_name='Disarmament and International Security')
        self.assertTrue(c.rubric == None)
        c.save()
        self.assertTrue(c.rubric != None)
        rubric_id = c.rubric.id
        c.rubric.grade_category_1 = "Overall paper quality"
        c.rubric.save()
        c.save()
        self.assertEquals(c.rubric.grade_category_1, "Overall paper quality")
        self.assertEquals(c.rubric.id, rubric_id)
        c.rubric = None
        c.save()
        self.assertFalse(c.rubric == None)
        self.assertFalse(c.rubric.id == rubric_id)


class CommitteeFeedbackTest(TestCase):
    def setUp(self):
        self.committee = Committee.objects.create(
            name='DISC', full_name='Disarmament and International Security')
        self.committee_feedback = CommitteeFeedback.objects.create(
            committee=self.committee,
            comment='Jake Tibbetts was literally awful as a person',
            rating=3,
            chair_1_name='Jake Tibbetts',
            chair_1_comment='He got mad at me for watching Pacific Rim the whole time',
            chair_1_rating=1, )

    def test_default_fields(self):
        self.assertFalse(self.committee == None)

    def test_unicode(self):
        self.assertEquals('DISC - Comment 1',
                          self.committee_feedback.__unicode__())


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
        assignments = [a[1:-1] for a in Assignment.objects.all().values_list()]
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

    def test_create_position_paper(self):
        '''Tests that an assigment creates a new position paper upon
           being saved for the first time, but not on subsequent saves.'''
        a = Assignment(committee_id=1, country_id=1, registration_id=1)
        self.assertTrue(a.paper == None)
        a.save()
        self.assertTrue(a.paper != None)
        paper_id = a.paper.id
        a.paper.graded = True
        a.paper.save()
        a.save()
        self.assertTrue(a.paper.graded)
        self.assertEquals(a.paper.id, paper_id)
        a.paper = None
        a.save()
        self.assertFalse(a.paper == None)
        self.assertFalse(a.paper.id == paper_id)


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

    def setUp(self):
        self.school = models.new_school(name='S1')
        self.registration = models.new_registration()
        self.assignment1 = models.new_assignment(registration=self.registration)
        self.assignment2 = models.new_assignment(registration=self.registration)

    def test_save(self):
        """
        A delegate's school field and a delegate's assignment's school field
        should be the same if they both exist on the delegate.
        """

        self.assertRaises(
            ValidationError,
            Delegate.objects.create,
            name="Test Delegate",
            school=self.school,
            assignment=self.assignment1)

    def test_unique(self):
        """
        Here we want to test three cases:
        1. That if two delegates from the same committee have assigned seats, they cannot have the same seat
        2. That if two delegates from different committees have assigned seats, they can have the same seat
        3. That two delegates can both have unassigned seats
        """

        delegate_1 = Delegate.objects.create(name='delegate1', 
                                             school=self.school, 
                                             assignment=self.assignment1,
                                             seat_number=1)

        # 1: Here, we are verifying that an error is raised
        self.assertRaises(
            ValidationError,
            Delegate.objects.create,
            name='bad_delegate',
            school=self.school,
            assignment=self.assignment1,
            seat_number=1)

        # 2: Here, we verify that the values are equal. If an error is raised, it will fail the test case.
        delegate_2 = Delegate.objects.create(name='delegate2', 
                                             school=self.school, 
                                             assignment=self.assignment2,
                                             seat_number=1)
        self.assertEquals(delegate_1.seat_number, delegate_2.seat_number)

        # 3: Create two delegates with default seat numbers.
        #    Assign them both to self.school and self.assignment1
        #    Name them whatever you want.
        delegate_3 = '''Your code here'''
        delegate_4 = '''Your code here'''

        # Check that delegate_3 and delegate_4 have the same seat number, 
        # and that it is the default unassigned seat number
        self.assertEquals('''Your code here''', '''Your code here''')
        self.assertEquals('''Your code here''', '''Your code here''')


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

    fixtures = ['conference']

    def setUp(self):
        self.position_paper = PositionPaper.objects.create()
        self.assignment = models.new_assignment(paper=self.position_paper)

    def test_default_values(self):
        self.assertEquals(self.position_paper.score_1, 0)
        self.assertEquals(self.position_paper.score_2, 0)
        self.assertEquals(self.position_paper.score_3, 0)
        self.assertEquals(self.position_paper.score_4, 0)
        self.assertEquals(self.position_paper.score_5, 0)
        self.assertFalse(self.position_paper.graded)

    def test_unicode(self):
        a = self.assignment
        self.assertEquals('%s %s %d' %
                          (a.committee.name, a.country.name, a.id),
                          self.position_paper.__unicode__())


class RubricTest(TestCase):
    def setUp(self):
        self.rubric = Rubric.objects.create()
        self.committee = models.new_committee(rubric=self.rubric)

    def test_default_fields(self):
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
        self.assertEquals(self.committee.name, self.rubric.__unicode__())



class SecretariatMemberTest(TestCase):
    def setUp(self):
        self.committee = Committee.objects.create(
            name='DISC', full_name='Disarmament and International Security')
        self.member = SecretariatMember.objects.create(
            name='Tibbalidoo', committee=self.committee)

    def test_default_fields(self):
        self.assertFalse(self.member.is_head_chair)

    def test_unicode(self):
        self.assertTrue(self.member.__unicode__() == 'Tibbalidoo')

class RoomTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(building_name='Dwinelle', room_number=55)

    def test_default_values(self):
        """
        Fill in where indicated with what the default values should be.
        """
        self.assertEquals(self.room.number_of_seats, '''Your code here''')

    def test_unicode(self):
        """
        FIll in what the unicode method you defiend earlier should return.
        """
        self.assertEquals(self.room.__unicode__(), '''Your code here''')

    def test_unique(self):
        """
        Two rooms cannot have the same room number and building.
        In the setUp method above a room was already created.
        Check that a new room cannot have the same building and room number as it.
        """
        self.assertRaises(
            ValidationError,
            Room.objects.create,
            building_name='''Your code here''',
            room_number='''Your code here'''
            )


class RoomCommentTest(TestCase):
    def setUp(self):
        """Your code here"""
        pass # Delete this

    def test_default_fields(self):
        """Your code here"""
        pass # Delete this

    def test_unicode(self):
        """Your code here"""
        pass # Delete this

