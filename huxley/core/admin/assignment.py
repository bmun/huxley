# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from huxley.core.models import Assignment, Committee, Country, School


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
        '''Loads new Assignments.'''
        assignments = request.FILES
        reader = csv.reader(assignments['csv'])

        def generate_assigments(reader):
            committees = {}
            countries = {}
            schools = {}
            for row in reader:
                if (len(row[4]) < 2): #ignore the first row because of headers
                    if row[2] in committees:
                        committee = committees[row[2]]
                    else:
                        committee = Committee.objects.get(name=row[2])
                        committees[row[2]] = committee
                    if row[3] in countries:
                        country = countries[row[3]]
                    else:
                        country = Country.objects.get(name=row[3])
                        countries[row[3]] = country
                    if row[0] in schools:
                        school = schools[row[0]]
                    else:
                        school = School.objects.get(name=row[0])
                        schools[row[0]] = school
                    yield (committee.id, country.id, school.id)

        Assignment.update_assignments(generate_assigments(reader))
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
