# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from huxley.core.models import Country


class CountryAdmin(admin.ModelAdmin):

    search_fields = ('name', )

    def load(self, request):
        '''Import a CSV file containing countries.'''
        countries = request.FILES
        reader = csv.reader(countries['csv'])
        for row in reader:
            c = Country(name=row[0], special=bool(row[1]))
            c.save()

        return HttpResponseRedirect(reverse('admin:core_country_changelist'))

    def get_urls(self):
        return super(CountryAdmin, self).get_urls() + [
            url(r'load',
                self.admin_site.admin_view(self.load),
                name='core_country_load'),
        ]
