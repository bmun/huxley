# Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from googleapiclient.discovery import build
from google.oauth2 import service_account

from huxley.core.models import Assignment, Delegate, School


class DelegateAdmin(admin.ModelAdmin):

    search_fields = ('name', )

    def get_rows(self):
        rows = []

        rows.append([
            'ID', 'Name', 'School', 'Committee', 'Country', 'Email', 'Waiver?',
            'Session One', 'Session Two', 'Session Three', 'Session Four'
        ])

        ordering = 'assignment__registration__school__name'
        for delegate in Delegate.objects.all().order_by(ordering):
            rows.append([
                str(delegate.id),
                str(delegate),
                str(delegate.school),
                str(delegate.committee),
                str(delegate.country),
                str(delegate.email), delegate.waiver_submitted,
                delegate.session_one, delegate.session_two,
                delegate.session_three, delegate.session_four
            ])
        return rows

    def roster(self, request):
        '''Return a CSV file representing the entire roster of registered
        delegates, including their committee, country, and school.'''
        roster = HttpResponse(content_type='text/csv')
        roster['Content-Disposition'] = 'attachment; filename="roster.csv"'
        writer = csv.writer(roster)
        for row in self.get_rows():
            writer.writerow(row)

        return roster

    def load(self, request):
        '''
        Loads new Assignments and/or updates assignments.
        CSV format: Name, Committee, Country, School, Email"
        '''
        existing_delegates = Delegate.objects.all()
        delegates = request.FILES
        reader = csv.reader(
            delegates['csv'].read().decode('utf-8').splitlines())
        assignments = {}
        for assignment in Assignment.objects.all():
            assignments[assignment.committee.name, assignment.country.name,
                        assignment.registration.school.name, ] = assignment

        for row in reader:
            if row:
                if row[1] == 'Committee':
                    continue
                school = School.objects.get(name=str(row[3]))
                assignment = assignments[str(row[1]), str(row[2]), row[3], ]
                email = str(row[4])
                delg = list(
                    Delegate.objects.filter(name=str(row[0]), email=email))
                if len(delg) == 1:
                    Delegate.objects.filter(name=str(
                        row[0]), email=email).update(assignment=assignment)
                else:
                    Delegate.objects.create(name=row[0],
                                            school=school,
                                            email=email,
                                            assignment=assignment)

        return HttpResponseRedirect(reverse('admin:core_delegate_changelist'))

    def confirm_waivers(self, request):
        '''Confirms delegate waivers'''
        waiver_responses = request.FILES
        reader = csv.reader(
            waiver_responses['csv'].read().decode('utf-8').splitlines())

        rows_to_write = []

        waiver_input_response = HttpResponse(content_type='text/csv')
        waiver_input_response[
            'Content-Disposition'] = 'attachment; filename="waiver_input_response.csv"'
        writer = csv.writer(waiver_input_response)

        no_exist = 0
        duplicate = 0
        success = 0

        for row in reader:
            if (not row or row[0] == "Email"):
                continue
            #rows: email(0), name(1), school(2), committee(3), country(4)
            email = row[0]
            name = row[1]
            school = row[2]
            committee = row[3]
            country = row[4]
            row = [email, name, school, committee, country]
            results = Delegate.objects.filter(email__iexact=email)
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

        writer.writerow(
            ['Email', 'Name', 'School', 'Committee', 'Country', 'Error'])

        for row in rows_to_write:
            writer.writerow(row)

        return waiver_input_response

    def sheets(self, request):
        if settings.SHEET_ID:
            SHEET_RANGE = 'Delegates!A1:K'
            # Store credentials
            creds = service_account.Credentials.from_service_account_file(
                settings.SERVICE_ACCOUNT_FILE, scopes=settings.SCOPES)
            
            service = build('sheets', 'v4', credentials=creds)
            
            response = service.spreadsheets().values().get(
                spreadsheetId=settings.SHEET_ID,
                range=SHEET_RANGE,
                majorDimension='ROWS').execute()
            
            for row in response['values'][1:]:
                delegate = Delegate.objects.get(id=row[0])
                if row[6] == "TRUE" or row[6] == "x":
                    delegate.waiver_submitted = True
                    delegate.save()

            data = self.get_rows()

            body = {
                'values': data,
            }
            response = service.spreadsheets().values().clear(
                spreadsheetId=settings.SHEET_ID,
                range=SHEET_RANGE,
            ).execute()
            service.spreadsheets().values().update(
                spreadsheetId=settings.SHEET_ID,
                range=SHEET_RANGE,
                valueInputOption='USER_ENTERED',
                body=body).execute()

        return HttpResponseRedirect(reverse('admin:core_delegate_changelist'))

    def get_urls(self):
        return super(DelegateAdmin, self).get_urls() + [
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
            url(
                r'confirm_waivers',
                self.admin_site.admin_view(self.confirm_waivers),
                name='core_delegate_confirm_waivers',
            ),
            url(
                r'sheets',
                self.admin_site.admin_view(self.sheets),
                name='core_delegate_sheets',
            ),
        ]
