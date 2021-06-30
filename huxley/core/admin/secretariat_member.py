# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import html

from huxley.core.models import Committee, SecretariatMember


class SecretariatMemberAdmin(admin.ModelAdmin):
    def load(self, request):
        '''Import a CSV file containing secretariat members.'''
        members = request.FILES
        reader = csv.reader(members['csv'].read().decode('utf-8').splitlines())
        failed_uploads = []
        for row in reader:
            if row and row[0] != 'Name':
                committee_check = Committee.objects.filter(name__exact=row[1]).exists()
                if committee_check:
                    row_committee = Committee.objects.get(name__exact=row[1])
                    head_chair = True if (len(row) > 2 and row[2] == "TRUE") else False
                    sm = SecretariatMember(
                        name=row[0], committee=row_committee, is_head_chair=head_chair)
                    sm.save()
                else:
                    failed_uploads.append(row)
        if failed_uploads:
            messages.error(
                request, 'Not all secretariat members could upload. These rows failed because the committee name could not be found: '
                    +  str(failed_uploads))

        return HttpResponseRedirect(
            reverse('admin:core_secretariatmember_changelist'))

    def get_urls(self):
        return super(SecretariatMemberAdmin, self).get_urls() + [
            url(r'load',
                self.admin_site.admin_view(self.load),
                name='core_secretariatmember_load'),
        ]
