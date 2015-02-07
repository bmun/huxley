# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from contextlib import closing

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.core.models import Assignment, Committee, Country, Delegate, School
from huxley.utils.test import TestFiles, TestSchools, TestUsers


class DelegateAdminTest(TestCase):

    def test_import(self):
        '''Test that the admin panel can import delegates. '''
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

        school = TestSchools.new_school()

        f = TestFiles.new_csv([
            ['Test School', '1', 'SPD', "Côte d'Ivoire", '2'],
            ['Test School', '1', 'USS', 'Barbara Boxer', '1'],
        ])

        with closing(f) as f:
            self.client.post(reverse('admin:core_assignment_load'), {'csv': f})

        self.assertTrue(Assignment.objects.filter(
            school=School.objects.get(name='Test School'),
            committee=Committee.objects.get(name='SPD'),
            country=Country.objects.get(name="Côte d'Ivoire")
        ).exists())
        self.assertTrue(Assignment.objects.filter(
            school=School.objects.get(name='Test School'),
            committee=Committee.objects.get(name='USS'),
            country=Country.objects.get(name='Barbara Boxer')
        ).exists())

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
