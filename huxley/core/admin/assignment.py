# Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf import settings
from django.conf.urls import url
from django.urls import reverse
from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import html

from googleapiclient.discovery import build
from google.oauth2 import service_account

from huxley.core.models import Assignment, Committee, Country


class AssignmentAdmin(admin.ModelAdmin):

    search_fields = ('country__name', 'committee__name',
                     'committee__full_name')

    def get_rows(self):
        rows = []
        rows.append(['Committee', 'Country'])

        for assignment in Assignment.objects.all().order_by('committee__name'):
            rows.append([
                str(item) for item in [
                    assignment.committee,
                    assignment.country
                ]
            ])

        return rows

    def list(self, request):
        '''Return a CSV file containing the current country assignments.'''
        assignments = HttpResponse(content_type='text/csv')
        assignments[
            'Content-Disposition'] = 'attachment; filename="assignments.csv"'
        writer = csv.writer(assignments)
        for row in self.get_rows():
            writer.writerow(row)

        return assignments

    def load(self, request):
        '''Loads new Assignments.'''
        assignments = request.FILES
        reader = csv.reader(
            assignments['csv'].read().decode('utf-8').splitlines())

        def get_model(model, name, cache):
            name = name.strip()
            if not name in cache:
                try:
                    cache[name] = model.objects.get(name=name)
                except model.DoesNotExist:
                    cache[name] = name
            return cache[name]

        def generate_assignments(reader):
            committees = {}
            countries = {}

            for row in reader:
                if len(row) == 0:
                    continue

                if (row[0] == 'Committee'
                        and row[1] == 'Country'):
                    continue  # skip the first row if it is a header

                while len(row) < 2:
                    row.append(
                        ""
                    )  # extend the row to have the minimum proper num of columns

                committee = get_model(Committee, row[0], committees)
                country = get_model(Country, row[1], countries)
                yield (committee, country)

        failed_rows = Assignment.update_assignments(
            generate_assignments(reader))
        if failed_rows:
            # Format the message with HTML to put each failed assignment on a new line
            messages.error(
                request,
                html.format_html(
                    'Assignment upload aborted. These assignments failed:<br/>'
                    + '<br/>'.join(failed_rows)))

        return HttpResponseRedirect(
            reverse('admin:core_assignment_changelist'))

    def sheets(self, request):
        if settings.SHEET_ID:
            SHEET_RANGE = 'Assignments!A1:B'
            # Store credentials
            creds = service_account.Credentials.from_service_account_file(
                settings.SERVICE_ACCOUNT_FILE, scopes=settings.SCOPES)

            data = self.get_rows()

            body = {
                'values': data,
            }

            service = build('sheets', 'v4', credentials=creds)
            response = service.spreadsheets().values().clear(
                spreadsheetId=settings.SHEET_ID,
                range=SHEET_RANGE,
            ).execute()

            response = service.spreadsheets().values().update(
                spreadsheetId=settings.SHEET_ID,
                range=SHEET_RANGE,
                valueInputOption='USER_ENTERED',
                body=body).execute()

        return HttpResponseRedirect(
            reverse('admin:core_assignment_changelist'))

    def get_urls(self):
        return super(AssignmentAdmin, self).get_urls() + [
            url(r'list',
                self.admin_site.admin_view(self.list),
                name='core_assignment_list'),
            url(
                r'load',
                self.admin_site.admin_view(self.load),
                name='core_assignment_load',
            ),
            # url(
            #     r'sheets',
            #     self.admin_site.admin_view(self.sheets),
            #     name='core_assignment_sheets',
            # ),
        ]
