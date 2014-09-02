# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from contextlib import closing

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.core.models import Committee
from huxley.utils.test import TestFiles, TestUsers


class CommitteeAdminTest(TestCase):

    def test_import(self):
        '''Test that the admin panel can import committees.'''
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
