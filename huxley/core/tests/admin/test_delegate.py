# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from contextlib import closing

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.core.models import Assignment, Committee, Country, Delegate, School
from huxley.utils.test import TestCommittees, TestCountries, TestFiles, TestSchools, TestUsers


class DelegateAdminTest(TestCase):

    def test_import(self):
        '''Test that the admin panel can import delegates. '''
        TestUsers.new_superuser(username='testuser', password='test')
        self.client.login(username='testuser', password='test')

        school = TestSchools.new_school()
        cm1 = TestCommittees.new_committee(name='SPD')
        cm2 = TestCommittees.new_committee(name='USS')
        co1 = TestCountries.new_country(name="Côte d'Ivoire")
        co2 = TestCountries.new_country(name='Barbara Boxer')
        Assignment.objects.create(committee=cm1, country=co1, school=school)
        Assignment.objects.create(committee=cm2, country=co2, school=school)

        f = TestFiles.new_csv([
            ['Name', 'Committee', 'Country', 'School'],
            ['John Doe', 'SPD', "Côte d'Ivoire", 'Test School'],
            ['Jane Doe', 'USS', 'Barbara Boxer', 'Test School'],
        ])

        with closing(f) as f:
            self.client.post(reverse('admin:core_delegate_load'), {'csv': f})

        self.assertTrue(Delegate.objects.filter(
            assignment=Assignment.objects.get(
                school=School.objects.get(name='Test School'),
                committee=Committee.objects.get(name='SPD'),
                country=Country.objects.get(name="Côte d'Ivoire")
            ),
            name='John Doe'
        ).exists())
        self.assertTrue(Delegate.objects.filter(
            assignment=Assignment.objects.get(
                school=School.objects.get(name='Test School'),
                committee=Committee.objects.get(name='USS'),
                country=Country.objects.get(name='Barbara Boxer')
            ),
            name='Jane Doe'
        ).exists())
