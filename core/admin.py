#!/usr/bin/env python

# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

import csv

from core.models import *
from django.contrib import admin
from django.http import HttpResponse

class DelegateAdmin(admin.ModelAdmin):
    def roster(self, request):
        roster = HttpResponse(content_type='text/csv')
        roster['Content-Disposition'] = 'attachment; filename="delegateroster.csv"'
        writer = csv.writer(roster)

        for delegate in Delegate.objects.all().order_by('delegateslot__assignment__school__name'):
            writer.writerow([
                delegate,
                delegate.get_committee(),
                delegate.get_country(),
                delegate.get_school()
            ])

        return roster

    def get_urls(self):
        from django.conf.urls.defaults import *
        urls = super(DelegateAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'roster',
                self.admin_site.admin_view(self.roster),
                name='core_delegate_roster',
            ),
        )
        return my_urls + urls


class AssignmentAdmin(admin.ModelAdmin):
    def list(self, request):
        assignments = HttpResponse(content_type='text/csv')
        assignments['Content-Disposition'] = 'attachment; filename="assignments.csv"'
        writer = csv.writer(assignments)

        for assignment in Assignment.objects.all().order_by('school__name', 'committee__name'):
            writer.writerow([assignment.school, assignment.committee, assignment.country])

        return assignments

    def get_urls(self):
        from django.conf.urls.defaults import *
        urls = super(AssignmentAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'list',
                self.admin_site.admin_view(self.list),
                name='core_assignment_list'
            ),
        )
        return my_urls + urls

admin.site.register(Conference)
admin.site.register(Country)
admin.site.register(School)
admin.site.register(Committee)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(CountryPreference)
admin.site.register(HelpQuestion)
admin.site.register(HelpCategory)
admin.site.register(DelegateSlot)
admin.site.register(Delegate, DelegateAdmin)