# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from contextlib import closing

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.core.models import SecretariatMember
from huxley.utils.test import models, TestFiles


class SecretariatMemberAdminTest(TestCase):
    def test_import(self):
        '''Test that the admin panel can import committees.'''
        models.new_superuser(username='testuser', password='test')
        self.client.login(username='testuser', password='test')

        committee = models.new_committee(name='ICJ')

        f = TestFiles.new_csv([
            ['Trent Gomberg', 'ICJ', ''], ['Ali Maloney', 'ICJ', 'True']
        ])

        with closing(f) as f:
            self.client.post(
                reverse('admin:core_secretariatmember_load'), {'csv': f})

        self.assertTrue(
            SecretariatMember.objects.filter(
                name='Trent Gomberg',
                committee=committee.id,
                is_head_chair=False).exists())
        self.assertTrue(
            SecretariatMember.objects.filter(
                name='Ali Maloney', committee=committee.id,
                is_head_chair=True).exists())
