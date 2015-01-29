# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from huxley.core.models import Assignment, Committee, Country, Delegate, School


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

        def upload_delegates(reader):
            assignments = {}
            header = False
            for row in reader:
                if not header:
                        header = True
                        continue
                assignment = Assignment.objects.get(committee=Committee.objects.get(name=row[1]), country=Country.objects.get(name=row[2]), school=School.objects.get(name=row[3]))
                d = Delegate(name=row[0], assignment=assignment)
                d.save()

        upload_delegates(reader)
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
