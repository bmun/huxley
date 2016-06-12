# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv
import Tkinter, tkMessageBox

from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from huxley.core.models import Assignment, Committee, Country, School


class AssignmentAdmin(admin.ModelAdmin):
    def list(self, request):
        '''Return a CSV file containing the current country assignments.'''
        assignments = HttpResponse(content_type='text/csv')
        assignments['Content-Disposition'] = 'attachment; filename="assignments.csv"'
        writer = csv.writer(assignments)
        writer.writerow([
                'School',
                'Committee',
                'Country',
                'Rejected'
            ])

        for assignment in Assignment.objects.all().order_by('school__name',
                                                            'committee__name'):
            writer.writerow([
                assignment.school,
                assignment.committee,
                assignment.country,
                assignment.rejected
            ])

        return assignments

    def load(self, request):
        '''Loads new Assignments.'''
        assignments = request.FILES
        reader = csv.reader(assignments['csv'])
        assigned = set()
        failed_rows = []

        def get_model(model, name, cache):
            if not name in cache:
                cache[name] = model.objects.get(name=name)
            return cache[name]

        def generate_assignments(reader):
            committees = {}
            countries = {}
            schools = {}

            for row in reader:
                if (row[0]=='School' and row[1]=='Committee' and row[2]=='Country'):
                    continue # skip the first row if it is a header

                while len(row) < 3:
                    row.append("") # extends the row to have the minimum proper num of columns
                if len(row) < 4:
                    rejected = False # allow for the rejected field to be null
                else:
                    rejected = (row[3].lower() == 'true') # use the provided value if admin provides it

                try:
                    committee = get_model(Committee, row[1], committees)
                    country = get_model(Country, row[2], countries)
                    school = get_model(School, row[0], schools)
                    yield (committee.id, country.id, school.id, rejected)
                except ObjectDoesNotExist:
                    yield (row[1], row[2], row[0], rejected)

    
        failed_rows = Assignment.update_assignments(generate_assignments(reader))
        if failed_rows:
            messages.error(request, 
                'Assignments aborted. These are the rows that failed with identification of the cells at fault: ' + ' | '.join(failed_rows))
        
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
                name='core_assignment_load',
            ),
        )
        return urls
