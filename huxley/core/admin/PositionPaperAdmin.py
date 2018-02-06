# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from huxley.core.models import PositionPaper


class PositionPaperAdmin(admin.ModelAdmin):
    def get_urls(self):
        return super(CommitteeAdmin, self).get_urls()
