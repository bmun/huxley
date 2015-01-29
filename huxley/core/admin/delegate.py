# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from huxley.core.models import Assignment, Delegate


class DelegateAdmin(admin.ModelAdmin):
    def roster(self, request):
        '''Return a CSV file representing the entire roster of registered
        delegates, including their committee, country, and school.'''
        roster = HttpResponse(content_type='text/csv')
        roster['Content-Disposition'] = 'attachment; filename="roster.csv"'
        writer = csv.writer(roster)

        ordering = 'assignment__school__name'
        for delegate in Delegate.objects.all().order_by(ordering):
            writer.writerow([
                delegate,
                delegate.committee,
                delegate.country,
                delegate.school
            ])

        return roster

    def load(self, request):
        '''Loads new Assignments.'''
        delegates = request.FILES
        reader = csv.reader(delegates['csv'])

        assignments = {}
        for assignment in Assignment.objects.all():
            assignments[
                assignment.committee.name.encode('ascii', 'ignore'),
                assignment.country.name.encode('ascii', 'ignore'),
                assignment.school.name, 
            ] = assignment
        for row in reader:
            if row[1] == 'Committee':
                continue
            assignment = assignments[
                            unicode(row[1], errors='ignore'),
                            unicode(row[2], errors='ignore'),
                            row[3], 
                          ]
            d = Delegate.objects.create(name=row[0], assignment=assignment)

        return HttpResponseRedirect(reverse('admin:core_delegate_changelist'))

    def get_urls(self):
        urls = super(DelegateAdmin, self).get_urls()
        urls += patterns('',
            url(
                r'roster',
                self.admin_site.admin_view(self.roster),
                name='core_delegate_roster',
            ),
            url(
                r'load',
                self.admin_site.admin_view(self.load),
                name='core_delegate_load',
            ),
        )
        return urls
