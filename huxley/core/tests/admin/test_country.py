# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from contextlib import closing

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.core.models import Country
from huxley.utils.test import TestFiles, TestUsers


class CountryAdminTest(TestCase):

    def test_import(self):
        '''Test that the admin panel can import countries. '''
        TestUsers.new_superuser(username='testuser', password='test')
        self.client.login(username='testuser', password='test')

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
