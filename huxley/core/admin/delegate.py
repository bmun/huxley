# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from huxley.core.models import Assignment, Delegate


class DelegateAdmin(admin.ModelAdmin):

    search_fields = ('name', )

    def roster(self, request):
        '''Return a CSV file representing the entire roster of registered
        delegates, including their committee, country, and school.'''
        roster = HttpResponse(content_type='text/csv')
        roster['Content-Disposition'] = 'attachment; filename="roster.csv"'
        writer = csv.writer(roster)
        writer.writerow([
            'Name', 'School', 'Committee', 'Country', 'Email', 'Session One',
            'Session Two', 'Session Three', 'Session Four'
        ])

        ordering = 'assignment__registration__school__name'
        for delegate in Delegate.objects.all().order_by(ordering):
            writer.writerow([
                delegate, delegate.school, delegate.committee,
                delegate.country, delegate.email, delegate.session_one,
                delegate.session_two, delegate.session_three,
                delegate.session_four
            ])

        return roster

    def load(self, request):
        '''Loads new Assignments.'''
        delegates = request.FILES
        reader = csv.reader(delegates['csv'])

        assignments = {}
        for assignment in Assignment.objects.all():
            assignments[assignment.committee.name.encode('ascii', 'ignore'),
                        assignment.country.name.encode('ascii', 'ignore'),
                        assignment.registration.school.name, ] = assignment
        for row in reader:
            if row[1] == 'Committee':
                continue
            assignment = assignments[unicode(
                row[1], errors='ignore'), unicode(
                    row[2], errors='ignore'), row[3], ]
            d = Delegate.objects.create(name=row[0], assignment=assignment)

        return HttpResponseRedirect(reverse('admin:core_delegate_changelist'))

    def confirm_waivers(self, request):
        '''Confirms delegate waivers'''
        waiver_responses = request.FILES
        reader = csv.reader(waiver_responses['csv'])

        rows_to_write = []

        waiver_input_response = HttpResponse(content_type='text/csv')
        waiver_input_response[
            'Content-Disposition'] = 'attachment; filename="waiver_input_response.csv"'
        writer = csv.writer(waiver_input_response)

        no_exist = 0
        duplicate = 0
        success = 0

        for row in reader:
            if (row[0] == "Email"):
                continue
            #rows: email(0), name(1), school(2), committee(3), country(4)
            email = row[0]
            name = row[1]
            school = row[2]
            committee = row[3]
            country = row[4]
            row = [email, name, school, committee, country]
            results = Delegate.objects.filter(email=email)
            if (results.count() == 0):
                row.append("Email does not exist")
                no_exist += 1
            elif (not results.count() == 1):
                row.append("Email is duplicated")
                duplicate += 1
            else:
                to_append = ""
                delegate = results[0]
                delegate.waiver_submitted = True
                delegate.save()
                row.append("Successfully waived")
                success += 1
                #log the successful add
            rows_to_write.append(row)

        num_total = Delegate.objects.all().count()
        num_submitted = Delegate.objects.filter(waiver_submitted=True).count()
        num_left = num_total - num_submitted

        writer.writerow(['Number of delegates', num_total])
        writer.writerow(['Number of non-pending waivers', num_submitted])
        writer.writerow(['Number of pending waivers', num_left])
        writer.writerow([])

        writer.writerow(['Number of \'Successfully waived\'', success])
        writer.writerow(['Number of \'Email does not exist\'', no_exist])
        writer.writerow(['Number of \'Email is duplicated\'', duplicate])
        writer.writerow([])

        writer.writerow([
            'Email', 'Name', 'School', 'Committee', 'Country', 'Error'
        ])

        for row in rows_to_write:
            writer.writerow(row)

        return waiver_input_response

    def get_urls(self):
        return super(DelegateAdmin, self).get_urls() + [
            url(r'roster',
                self.admin_site.admin_view(self.roster),
                name='core_delegate_roster', ),
            url(r'load',
                self.admin_site.admin_view(self.load),
                name='core_delegate_load', ),
            url(r'confirm_waivers',
                self.admin_site.admin_view(self.confirm_waivers),
                name='core_delegate_confirm_waivers', ),
        ]
