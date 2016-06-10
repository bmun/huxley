# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv
import Tkinter, tkMessageBox

from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import FieldError

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

        def get_model(model, name, cache):
            if not name in cache:
                cache[name] = model.objects.get(name=name)
            return cache[name]

        def get_bad_columns(row):
            bad_columns = set()
            if not Committee.objects.filter(name=row[1]).exists():
                bad_columns.add(1)
            if not Country.objects.filter(name=row[2]).exists():
                bad_columns.add(2)
            if not School.objects.filter(name=row[0]).exists():
                bad_columns.add(0)
            return bad_columns

        def create_assignments(reader):
            committees = {}
            countries = {}
            schools = {}
            assigned = set()
            successful_rows = []
            failed_rows = []

            for row in reader:
                if (row[0]=='School' and row[1]=='Committee' and row[2]=='Country'):
                    continue # skip the first row if it is a header
                
                while len(row) < 3:
                    row.append("") # extends the row to have the minimum proper num of columns

                bad_columns = get_bad_columns(row)
                already_assigned = (row[1], row[2]) in assigned
                
                if len(row) < 4:
                    rejected = False # allow for the rejected field to be null
                else:
                    rejected = (row[3].lower() == 'true') # use the provided value if admin provides it
                
                if not bad_columns and not already_assigned:
                    committee = get_model(Committee, row[1], committees)
                    country = get_model(Country, row[2], countries)
                    school = get_model(School, row[0], schools)
                    assigned.add((row[1], row[2]))
                    successful_rows.append((committee.id, country.id, school.id, rejected))
                else:
                    for col in bad_columns:
                        row[col] = row[col] + ' - INVALID'
                    
                    if already_assigned:
                        row[1] = row[1] + ' - ALREADY ASSIGNED'
                        row[2] = row[2] + ' - ALREADY ASSIGNED'
                    failed_rows.append(str((row[0], row[1], row[2], str(rejected))))
            return successful_rows, failed_rows

        successful_rows, failed_rows = create_assignments(reader)
        if not failed_rows:
            Assignment.update_assignments(successful_rows)
            return HttpResponseRedirect(reverse('admin:core_assignment_changelist'))
        else:
            messages.error(request, 
                'Assignments aborted.\nThese are the rows that failed with identification of the cells at fault:\n' + ', \n'.join(failed_rows))
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
