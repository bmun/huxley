# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from huxley.core.models import Committee, SecretariatMember


class SecretariatMemberAdmin(admin.ModelAdmin):
    def load(self, request):
        '''Import a CSV file containing secretariat members.'''
        # IMPORTANT: If the CSV file requirements change, make sure to update huxley/templates/admin/core/secretariatmember/change_list.html
        members = request.FILES
        reader = csv.reader(members['csv'].read().decode('utf-8').splitlines())
        for row in reader:
            row_committee = Committee.objects.get(name__exact=row[1])
            head_chair = True if (len(row) > 2 and row[2] == "TRUE") else False
            sm = SecretariatMember(
                name=row[0], committee=row_committee, is_head_chair=head_chair)
            sm.save()

        return HttpResponseRedirect(
            reverse('admin:core_secretariatmember_changelist'))

    def get_urls(self):
        return super(SecretariatMemberAdmin, self).get_urls() + [
            url(r'load',
                self.admin_site.admin_view(self.load),
                name='core_secretariatmember_load'),
        ]
