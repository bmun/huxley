# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from huxley.core.models import Committee
from huxley.core.models import Rubric


class CommitteeAdmin(admin.ModelAdmin):
    def load(self, request):
        '''Import a CSV file containing committees.'''
        # IMPORTANT: If the CSV file requirements change, make sure to update huxley/templates/admin/core/committee/change_list.html
        committees = request.FILES
        reader = csv.reader(committees['csv'].read().decode('utf-8').splitlines())
        for row in reader:
            if row and row[0] != 'Name':
                special = False if not row[3] or row[3].strip() == '0' or row[3].strip().lower() == 'false' or row[3].strip().lower() == 'n' else True
                com = Committee(name=row[0],
                                full_name=row[1],
                                delegation_size=int(row[2]),
                                special=special)
                com.save()

        return HttpResponseRedirect(reverse('admin:core_committee_changelist'))

    def get_urls(self):
        return super(CommitteeAdmin, self).get_urls() + [
            url(
                r'load',
                self.admin_site.admin_view(self.load),
                name='core_committee_load'
            ),
        ]
    
    def delete_model(self, request, obj):
        '''Deletes Rubric objects when individual committees are deleted'''
        super().delete_model(request, obj)
        Rubric.objects.filter(committee = None).delete()

    def delete_queryset(self, request, queryset):
        '''Deletes Rubric objects when queryset of committees are deleted'''
        super().delete_queryset(request, queryset)
        Rubric.objects.filter(committee = None).delete()
