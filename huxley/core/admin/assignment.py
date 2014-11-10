# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from huxley.core.models import Assignment, Committee, Country
from xlrd import open_workbook


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

    def load(self, request):
        '''Loads Committees, Countries and Assignments and sweeps old ones.'''
        assignments = request.FILES
        print(assignments)
        s = open_workbook(assignments['excel'].name).sheet_by_index(0)

        country_range = s.nrows
        committee_range = 22

        Country.objects.all().delete()
        for row in range(3, country_range):
            Country.objects.get_or_create(name=s.cell(row, 0).value, special=(True if row > 154 else False))

        Committee.objects.all().delete()
        for col in range(1, committee_range):
            Committee.objects.get_or_create(name=s.cell(1, col).value, full_name=s.cell(2, col).value, delegation_size=(1 if s.cell(0, col).value == 'SINGLE' else 2), special=(True if (col > 13 and col != 21) else False))

        Assignment.objects.all().delete()
        for row in range(3, country_range):
            for col in range(1, committee_range):
                if s.cell(row, col).value:
                    country = Country.objects.get(name=s.cell(row, 0).value)
                    committee = Committee.objects.get(name=s.cell(1, col).value)
                    assignment = Assignment(committee=committee, country=country)
                    assignment.save()

        return HttpResponseRedirect(reverse('admin:core_assignment_changelist'))

    def get_urls(self):
        urls = super(AssignmentAdmin, self).get_urls()
        urls += patterns('',
            url(
                r'list',
                self.admin_site.admin_view(self.list),
                name='core_assignment_list'
            ),
            url(
                r'load',
                self.admin_site.admin_view(self.load),
                name='core_assignment_load'
            )
        )
        return urls
