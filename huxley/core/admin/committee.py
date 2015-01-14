# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from huxley.core.models import Committee


class CommitteeAdmin(admin.ModelAdmin):
    def load(self, request):
        '''Import a CSV file containing committees.'''
        committees = request.FILES
        reader = csv.reader(committees['csv'])
        for row in reader:
            com = Committee(name=row[0],
                            full_name=row[1],
                            delegation_size=int(row[2]),
                            special=bool(row[3]))
            com.save()

        return HttpResponseRedirect(reverse('admin:core_committee_changelist'))

    def get_urls(self):
        urls = super(CommitteeAdmin, self).get_urls()
        urls += patterns('',
            url(
                r'load',
                self.admin_site.admin_view(self.load),
                name='core_committee_load'
            ),
        )
        return urls
