# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from googleapiclient.discovery import build
from google.oauth2 import service_account

from huxley.core.models import Note


class NotesAdmin(admin.ModelAdmin):

    def get_rows(self):
        '''Return the rows of data for huxley notes.'''
        rows = []
        rows.append(['timestamp', 'sender', 'sender is chair?', 'recipient',
                    'message'])

        for note in Note.objects.all().order_by(
                'timestamp'):
            rows.append([
                str(item) for item in [
                    note.timestamp, note.sender, note.is_chair, note.recipient, note.msg
                ]
            ])

        return rows

    def list(self, request):
        '''Return a CSV file containing the huxley notes.'''
        notes = HttpResponse(content_type='text/csv')
        notes[
            'Content-Disposition'] = 'attachment; filename="notes.csv"'
        writer = csv.writer(notes)
        for row in self.get_rows():
            writer.writerow(row)

        return notes

    def sheets(self, request):
        if settings.SHEET_ID:
            SHEET_RANGE = 'Notes!A1:E'
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
            reverse('admin:core_note_changelist'))

    def get_urls(self):
        return super(NotesAdmin, self).get_urls() + [
            url(r'list',
                self.admin_site.admin_view(self.list),
                name='core_note_list'),
            url(
                r'sheets',
                self.admin_site.admin_view(self.sheets),
                name='core_note_sheets',
            ),
        ]
