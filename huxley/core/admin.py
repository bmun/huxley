#!/usr/bin/env python

# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
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


class CountryAdmin(admin.ModelAdmin):
    def load(self, request):
        '''Import a CSV file containing countries.'''
        countries = request.FILES
        reader = csv.reader(countries['csv'])
        for row in reader:
            c = Country(name=row[0],
                        special=bool(row[1]))
            c.save()

        return HttpResponse(reverse('admin:core_country_changelist'))

    def get_urls(self):
        urls = super(CountryAdmin, self).get_urls()
        urls += patterns('',
            url(
                r'load',
                self.admin_site.admin_view(self.load),
                name='core_country_load'
            ),
        )
        return urls


admin.site.register(Conference)
admin.site.register(Country, CountryAdmin)
admin.site.register(School)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(CountryPreference)
admin.site.register(HelpQuestion)
admin.site.register(HelpCategory)
admin.site.register(DelegateSlot)
admin.site.register(Delegate, DelegateAdmin)
