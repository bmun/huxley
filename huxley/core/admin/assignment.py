# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponse

from huxley.core.models import Assignment


class AssignmentAdmin(admin.ModelAdmin):
    def list(self, request):
        '''Return a CSV file containing the current country assignments.'''
        assignments = HttpResponse(content_type='text/csv')
        assignments['Content-Disposition'] = 'attachment; filename="assignments.csv"'
        writer = csv.writer(assignments)

        for assignment in Assignment.objects.all().order_by('school__name',
                                                            'committee__name'):
            writer.writerow([
                assignment.school,
                assignment.committee,
                assignment.country
            ])

        return assignments

    def get_urls(self):
        urls = super(AssignmentAdmin, self).get_urls()
        urls += patterns('',
            url(
                r'list',
                self.admin_site.admin_view(self.list),
                name='core_assignment_list'
            ),
        )
        return urls
