# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase

from huxley.core.models import *
from huxley.core.admin import CommitteeAdmin
from huxley.utils.test import TestUsers

from datetime import date
from mock import Mock

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
    """ Tests that the admin panel can import committees. """

    def test_create_committee(self):
        """Tests the functionality of importing a committee. """
        csv_data = [
            'DISC,Disarmament and International Security,200,',
            'WHO,World Health Organization,200,',
            'USS,United States Senate,100,True'
        ]
        c = CommitteeAdmin(Committee, None)
        c.create_committees(csv_data)
        com1 = Committee.objects.get(name='DISC')
        com2 = Committee.objects.get(name='WHO')
        com3 = Committee.objects.get(name='USS')
        self.assertEquals(com1.name,'DISC')
        self.assertEquals(com1.full_name,
            'Disarmament and International Security')
        self.assertEquals(com1.delegation_size, 200)
        self.assertEquals(com1.special, False)
        self.assertEquals(com2.name, 'WHO')
        self.assertEquals(com2.full_name, 'World Health Organization')
        self.assertEquals(com2.delegation_size, 200)
        self.assertEquals(com2.special, False)
        self.assertEquals(com3.name, 'USS')
        self.assertEquals(com3.full_name, 'United States Senate')
        self.assertEquals(com3.delegation_size, 100)
        self.assertEquals(com3.special, True)

    def test_superuser(self):
        f = open('test_data.csv', 'w')
        writer = csv.writer(f)
        writer.writerow([
            'SPD',
            'Special Political and Decolonization',
            200,
            ''
        ])
        f.close()
        user = TestUsers.new_superuser()
        self.client.login(username='testuser', password='test')
        with open('test_data.csv') as fp:
            self.client.post(reverse('admin:core_committee_load'),
                {'name': 'committees', 'csv': fp})
        com = Committee.objects.get(name='SPD')
        self.assertEquals(com.name, 'SPD')
        self.assertEquals(com.full_name, 'Special Political and Decolonization')
        self.assertEquals(com.delegation_size, 200)
        self.assertEquals(com.special, False)

