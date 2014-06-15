# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from contextlib import closing
from datetime import date

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.core.models import *
from huxley.utils.test import TestFiles, TestUsers


class ConferenceTest(TestCase):

    conference = Conference.objects.create(
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

    country = Country.objects.create(name='Lolville')

    def test_default_fields(self):
        """ Tests that fields with default values are correctly set. """
        self.assertFalse(self.country.special)

    def test_unicode(self):
        """ Tests that the object's __unicode__ outputs correctly. """
        self.assertTrue(self.country.__unicode__() == 'Lolville')


class CommitteeTest(TestCase):

    committee = Committee.objects.create(
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
            ['SPD', 'Special Pôlitical and Decolonization', 2, '']
        ])

        with closing(f) as f:
            self.client.post(reverse('admin:core_committee_load'), {'csv': f})

        self.assertTrue(Committee.objects.filter(
            name='SPD',
            full_name='Special Pôlitical and Decolonization',
            delegation_size=2,
            special=False
        ).exists())
