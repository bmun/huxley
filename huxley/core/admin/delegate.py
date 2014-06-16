# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponse

from huxley.core.models import Delegate


class DelegateAdmin(admin.ModelAdmin):
    def roster(self, request):
        '''Return a CSV file representing the entire roster of registered
        delegates, including their committee, country, and school.'''
        roster = HttpResponse(content_type='text/csv')
        roster['Content-Disposition'] = 'attachment; filename="roster.csv"'
        writer = csv.writer(roster)

        ordering = 'delegate_slot__assignment__school__name'
        for delegate in Delegate.objects.all().order_by(ordering):
            writer.writerow([
                delegate,
                delegate.committee,
                delegate.country,
                delegate.school
            ])

        return roster

    def get_urls(self):
        urls = super(DelegateAdmin, self).get_urls()
        urls += patterns('',
            url(
                r'roster',
                self.admin_site.admin_view(self.roster),
                name='core_delegate_roster',
            ),
        )
        return urls
