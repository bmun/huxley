# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from contextlib import closing

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.core.models import Assignment, Committee, Country, School
from huxley.utils.test import TestCommittees, TestCountries, TestFiles, TestSchools, TestUsers


class AssignmentAdminTest(TestCase):

    def test_import(self):
        '''Test that the admin panel can import Assignments.'''
        TestUsers.new_superuser(username='testuser', password='test')
        self.client.login(username='testuser', password='test')

        school = TestSchools.new_school()
        cm1 = TestCommittees.new_committee(name='SPD')
        cm2 = TestCommittees.new_committee(name='USS')
        co1 = TestCountries.new_country(name="Côte d'Ivoire")
        co2 = TestCountries.new_country(name='Barbara Boxer')

        f = TestFiles.new_csv([
            ['Test School', 'SPD', "Côte d'Ivoire"],
            ['Test School', 'USS', 'Barbara Boxer']
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
