# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from huxley.core.models import PositionPaper


class PositionPaperAdmin(admin.ModelAdmin):

    search_fields = (
        'assignment__committee__name',
        'assignment__country__name'
    )

    def get_urls(self):
        return super(PositionPaperAdmin, self).get_urls()
