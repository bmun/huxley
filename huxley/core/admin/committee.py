# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from huxley.core.models import Committee


class CommitteeAdmin(admin.ModelAdmin):
    def load(self, request):
        '''Import a CSV file containing committees.'''
        committees = request.FILES
        reader = csv.reader(committees['csv'].read().decode('utf-8').splitlines())
        for row in reader:
            if row:
                special = False if row[3] == '0' or row[3] == 'False' or not row[3] else True
                com = Committee(name=row[0],
                                full_name=row[1],
                                delegation_size=int(row[2]),
                                special=bool(int(row[3])))
                com.save()

        return HttpResponseRedirect(reverse('admin:core_committee_changelist'))

    def get_urls(self):
        return super(CommitteeAdmin, self).get_urls() + [
            url(
                r'load',
                self.admin_site.admin_view(self.load),
                name='core_committee_load'
            ),
        ]
