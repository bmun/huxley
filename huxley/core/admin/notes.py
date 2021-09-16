# Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from googleapiclient.discovery import build

from huxley.core.models import Note


class NotesAdmin(admin.ModelAdmin):

    def get_rows(self):
        '''Return the rows of data for huxley notes.'''
        rows = []
        rows.append(['is_chair', 'sender_receiver',
                    'timestamp', 'msg', 'sender'])

        for note in Note.objects.all().order_by(
                'timestamp'):
            rows.append([
                str(item) for item in [
                    note.is_chair, note, note.timestamp, note.msg, note.sender
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

    def get_urls(self):
        return super(NotesAdmin, self).get_urls() + [
            url(r'list',
                self.admin_site.admin_view(self.list),
                name='core_note_list'),
        ]
