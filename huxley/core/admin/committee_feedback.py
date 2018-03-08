# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from huxley.core.models import CommitteeFeedback


class CommitteeFeedbackAdmin(admin.ModelAdmin):

    search_fields = ('committee__name', )

    def list(self, request):
        '''Return a CSV file containing all committee feedback.'''
        feedbacks = HttpResponse(content_type='text/csv')
        feedbacks[
            'Content-Disposition'] = 'attachment; filename="feedback.csv"'
        writer = csv.writer(feedbacks)
        writer.writerow([
            'Committee',
            'General Rating',
            'General Comment',
            'Chair 1',
            'Chair 1 Rating',
            'Chair 1 Comment',
            'Chair 2 Name',
            'Chair 2 Rating',
            'Chair 2 Comment',
            'Chair 3 Name',
            'Chair 3 Rating',
            'Chair 3 Comment',
            'Chair 4 Name',
            'Chair 4 Rating',
            'Chair 4 Comment',
            'Chair 5 Name',
            'Chair 5 Rating',
            'Chair 5 Comment',
            'Chair 6 Name',
            'Chair 6 Rating',
            'Chair 6 Comment',
            'Chair 7 Name',
            'Chair 7 Rating',
            'Chair 7 Comment',
            'Chair 8 Name',
            'Chair 8 Rating',
            'Chair 8 Comment',
            'Chair 9 Name',
            'Chair 9 Rating',
            'Chair 9 Comment',
            'Chair 10 Name',
            'Chair 10 Rating',
            'Chair 10 Comment',
        ])

        for feedback in CommitteeFeedback.objects.all().order_by(
                'committee__name'):
            writer.writerow([
                feedback.committee.name.encode('utf8'),
                feedback.rating,
                feedback.comment.encode('utf8'),
                feedback.chair_1_name.encode('utf8'),
                feedback.chair_1_rating,
                feedback.chair_1_comment.encode('utf8'),
                feedback.chair_2_name.encode('utf8'),
                feedback.chair_2_rating,
                feedback.chair_2_comment.encode('utf8'),
                feedback.chair_3_name.encode('utf8'),
                feedback.chair_3_rating,
                feedback.chair_3_comment.encode('utf8'),
                feedback.chair_4_name.encode('utf8'),
                feedback.chair_4_rating,
                feedback.chair_4_comment.encode('utf8'),
                feedback.chair_5_name.encode('utf8'),
                feedback.chair_5_rating,
                feedback.chair_5_comment.encode('utf8'),
                feedback.chair_6_name.encode('utf8'),
                feedback.chair_6_rating,
                feedback.chair_6_comment.encode('utf8'),
                feedback.chair_7_name.encode('utf8'),
                feedback.chair_7_rating,
                feedback.chair_7_comment.encode('utf8'),
                feedback.chair_8_name.encode('utf8'),
                feedback.chair_8_rating,
                feedback.chair_8_comment.encode('utf8'),
                feedback.chair_9_name.encode('utf8'),
                feedback.chair_9_rating,
                feedback.chair_9_comment.encode('utf8'),
                feedback.chair_10_name.encode('utf8'),
                feedback.chair_10_rating,
                feedback.chair_10_comment.encode('utf8')
            ])

        return feedbacks

    def get_urls(self):
        return super(CommitteeFeedbackAdmin, self).get_urls() + [
            url(r'list',
                self.admin_site.admin_view(self.list),
                name='core_committeefeedback_list')
        ]
