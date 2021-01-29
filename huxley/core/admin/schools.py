# Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from googleapiclient.discovery import build
from google.oauth2 import service_account

from huxley.core.models import School


class SchoolAdmin(admin.ModelAdmin):

    search_fields = ('name', )

    def get_rows(self):
        rows = []
        rows.append([
            "ID",
            "Name",
            "Address",
            "City",
            "State",
            "Zip Code",
            "Country",
            "Primary Name",
            "Primary Gender",
            "Primary Email",
            "Primary Phone",
            "Primary Type",
            "Secondary Name",
            "Secondary Gender",
            "Secondary Email",
            "Secondary Phone",
            "Secondary Type",
            "Program Type",
            "Times Attended",
            "International",
        ])

        for school in School.objects.all().order_by('name'):
            rows.append([
                str(field) for field in [
                    school.id,
                    school.name,
                    school.address,
                    school.city,
                    school.state,
                    school.zip_code,
                    school.country,
                    school.primary_name,
                    school.primary_gender,
                    school.primary_email,
                    school.primary_phone,
                    school.primary_type,
                    school.secondary_name,
                    school.secondary_gender,
                    school.secondary_email,
                    school.secondary_phone,
                    school.secondary_type,
                    school.program_type,
                    school.times_attended,
                    school.international,
                ]
            ])
        return rows

    def info(self, request):
        ''' Returns a CSV file containing the current set of
            Schools in our database with all of its fields. '''
        schools = HttpResponse(content_type='text/csv')
        schools['Content-Disposition'] = 'attachment; filename="schools.csv"'
        writer = csv.writer(schools)
        for row in self.get_rows():
            writer.writerow(row)

        return schools

    def sheets(self, request):
        if settings.SHEET_ID:
            SHEET_RANGE = 'Schools!A1:T'
            # Store credentials
            creds = service_account.Credentials.from_service_account_file(
                settings.SERVICE_ACCOUNT_FILE, scopes=settings.SCOPES)

            data = self.get_rows()

            body = {
                'values': data,
            }

            service = build('sheets', 'v4', credentials=creds)
            response = service.spreadsheets().values().update(
                spreadsheetId=settings.SHEET_ID,
                range=SHEET_RANGE,
                valueInputOption='USER_ENTERED',
                body=body).execute()

        return HttpResponseRedirect(reverse('admin:core_school_changelist'))

    def get_urls(self):
        return super(SchoolAdmin, self).get_urls() + [
            url(
                r'info',
                self.admin_site.admin_view(self.info),
                name='core_school_info',
            ),
            url(
                r'sheets',
                self.admin_site.admin_view(self.sheets),
                name='core_school_sheets',
            ),
        ]
