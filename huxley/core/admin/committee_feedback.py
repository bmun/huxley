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

from huxley.core.models import CommitteeFeedback


class CommitteeFeedbackAdmin(admin.ModelAdmin):

    search_fields = ('committee__name', )

    def get_rows(self):
        rows = []
        rows.append([
            'Committee', 'General Rating', 'General Comment', 'Chair 1',
            'Chair 1 Rating', 'Chair 1 Comment', 'Chair 2 Name',
            'Chair 2 Rating', 'Chair 2 Comment', 'Chair 3 Name',
            'Chair 3 Rating', 'Chair 3 Comment', 'Chair 4 Name',
            'Chair 4 Rating', 'Chair 4 Comment', 'Chair 5 Name',
            'Chair 5 Rating', 'Chair 5 Comment', 'Chair 6 Name',
            'Chair 6 Rating', 'Chair 6 Comment', 'Chair 7 Name',
            'Chair 7 Rating', 'Chair 7 Comment', 'Chair 8 Name',
            'Chair 8 Rating', 'Chair 8 Comment', 'Chair 9 Name',
            'Chair 9 Rating', 'Chair 9 Comment', 'Chair 10 Name',
            'Chair 10 Rating', 'Chair 10 Comment', 'Perception of Berkeley',
            'Money Spent'
        ])

        for feedback in CommitteeFeedback.objects.all().order_by(
                'committee__name'):
            rows.append([
                feedback.committee.name, feedback.rating, feedback.comment,
                feedback.chair_1_name, feedback.chair_1_rating,
                feedback.chair_1_comment, feedback.chair_2_name,
                feedback.chair_2_rating, feedback.chair_2_comment,
                feedback.chair_3_name, feedback.chair_3_rating,
                feedback.chair_3_comment, feedback.chair_4_name,
                feedback.chair_4_rating, feedback.chair_4_comment,
                feedback.chair_5_name, feedback.chair_5_rating,
                feedback.chair_5_comment, feedback.chair_6_name,
                feedback.chair_6_rating, feedback.chair_6_comment,
                feedback.chair_7_name, feedback.chair_7_rating,
                feedback.chair_7_comment, feedback.chair_8_name,
                feedback.chair_8_rating, feedback.chair_8_comment,
                feedback.chair_9_name, feedback.chair_9_rating,
                feedback.chair_9_comment, feedback.chair_10_name,
                feedback.chair_10_rating, feedback.chair_10_comment,
                feedback.berkeley_perception, feedback.money_spent
            ])
        return rows

    def list(self, request):
        '''Return a CSV file containing all committee feedback.'''
        feedbacks = HttpResponse(content_type='text/csv')
        feedbacks[
            'Content-Disposition'] = 'attachment; filename="feedback.csv"'
        writer = csv.writer(feedbacks)
        for row in self.get_rows():
            writer.writerow(row)

        return feedbacks

    def sheets(self, request):
        if settings.SHEET_ID:
            SHEET_RANGE = 'Feedback!A1:AI'
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
            reverse('admin:core_committeefeedback_changelist'))

    def get_urls(self):
        return super(CommitteeFeedbackAdmin, self).get_urls() + [
            url(r'list',
                self.admin_site.admin_view(self.list),
                name='core_committeefeedback_list'),
            url(
                r'sheets',
                self.admin_site.admin_view(self.sheets),
                name='core_committeefeedback_sheets',
            ),
        ]
