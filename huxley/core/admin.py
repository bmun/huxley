#!/usr/bin/env python

# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from huxley.core.models import *

class DelegateAdmin(admin.ModelAdmin):
    def roster(self, request):
        """ Returns a CSV file representing the entire roster of
            registered delegates, including their committee, country,
            and school. """
        roster = HttpResponse(content_type='text/csv')
        roster['Content-Disposition'] = 'attachment; filename="delegateroster.csv"'
        writer = csv.writer(roster)

        for delegate in Delegate.objects.all().order_by('delegate_slot__assignment__school__name'):
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


class AssignmentAdmin(admin.ModelAdmin):
    def list(self, request):
        """ Returns a CSV file containing the current set of
            country assignments. """
        assignments = HttpResponse(content_type='text/csv')
        assignments['Content-Disposition'] = 'attachment; filename="assignments.csv"'
        writer = csv.writer(assignments)

        for assignment in Assignment.objects.all().order_by('school__name', 'committee__name'):
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

class CommitteeAdmin(admin.ModelAdmin):
    def load(self, request):
        """ Imports a CSV file containing committeess. """
        print("loading")
        committees = request.FILES
        self.create_committees(committees['csv'])
        return HttpResponseRedirect('/admin/core/committee/')

    def create_committees(self, csv_data):
        reader = csv.reader(csv_data)
        for row in reader:
            com = Committee(name=row[0],
                            full_name=row[1],
                            delegation_size=row[2],
                            special=row[3],)
            com.save()

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



admin.site.register(Conference)
admin.site.register(Country)
admin.site.register(School)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(CountryPreference)
admin.site.register(HelpQuestion)
admin.site.register(HelpCategory)
admin.site.register(DelegateSlot)
admin.site.register(Delegate, DelegateAdmin)
