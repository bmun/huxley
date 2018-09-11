# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from huxley.core.models import Committee, SecretariatMember


class SecretariatMemberAdmin(admin.ModelAdmin):
    def load(self, request):
        '''Import a CSV file containing secretariat members.'''
        members = request.FILES
        reader = csv.reader(members['csv'])
        for row in reader:
            row_committee = Committee.objects.get(name__exact=row[1])
            sm = SecretariatMember(
                name=row[0],
                committee=row_committee,
                is_head_chair=bool(row[2]))
            sm.save()

        return HttpResponseRedirect(
            reverse('admin:core_secretariatmember_changelist'))

    def get_urls(self):
        return super(SecretariatMemberAdmin, self).get_urls() + [
            url(r'load',
                self.admin_site.admin_view(self.load),
                name='core_secretariatmember_load'),
        ]
