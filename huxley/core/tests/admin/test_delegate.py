# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

# -*- coding: utf-8 -*-

from contextlib import closing

from django.urls import reverse
from django.test import TestCase

from huxley.core.models import Assignment, Committee, Country, Delegate, School
from huxley.utils.test import models, TestFiles


class DelegateAdminTest(TestCase):

    fixtures = ['conference']

    def test_import(self):
        '''Test that the admin panel can import delegates. '''
        models.new_superuser(username='testuser', password='test')
        self.client.login(username='testuser', password='test')

        registration = models.new_registration()
        cm1 = models.new_committee(name='SPD')
        cm2 = models.new_committee(name='USS')
        co1 = models.new_country(name="Côte d'Ivoire")
        co2 = models.new_country(name='Barbara Boxer')
        Assignment.objects.create(
            committee=cm1, country=co1, registration=registration)
        Assignment.objects.create(
            committee=cm2, country=co2, registration=registration)

        f = TestFiles.new_csv([
            ['Name', 'Committee', 'Country', 'School', 'Email'],
            ['John Doe', 'SPD', "Côte d'Ivoire", 'Test School', 'test@bmun.org'],
            ['Jane Doe', 'USS', 'Barbara Boxer', 'Test School', 'test@bmun.org'],
        ])

        with closing(f) as f:
            self.client.post(reverse('admin:core_delegate_load'), {'csv': f})

        self.assertTrue(
            Delegate.objects.filter(
                assignment=Assignment.objects.get(
                    registration=registration,
                    committee=Committee.objects.get(name='SPD'),
                    country=Country.objects.get(name="Côte d'Ivoire")),
                name='John Doe').exists())
        self.assertTrue(
            Delegate.objects.filter(
                assignment=Assignment.objects.get(
                    registration=registration,
                    committee=Committee.objects.get(name='USS'),
                    country=Country.objects.get(name='Barbara Boxer')),
                name='Jane Doe').exists())
