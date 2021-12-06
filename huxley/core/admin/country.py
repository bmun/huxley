# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from huxley.core.models import Country


class CountryAdmin(admin.ModelAdmin):

    search_fields = ('name', )

    def load(self, request):
        '''Import a CSV file containing countries.'''
        # IMPORTANT: If the CSV file requirements change, make sure to update huxley/templates/admin/core/country/change_list.html
        countries = request.FILES
        reader = csv.reader(countries['csv'].read().decode('utf-8').splitlines())
        for row in reader:
            special = False if not row[1] or row[1].strip() == '0' or row[1].strip().lower() == 'false' or row[1].strip().lower() == 'n' else True
            print(row[1])
            c = Country(name=row[0], special=special)
            c.save()

        return HttpResponseRedirect(reverse('admin:core_country_changelist'))

    def get_urls(self):
        return super(CountryAdmin, self).get_urls() + [
            url(r'load',
                self.admin_site.admin_view(self.load),
                name='core_country_load'),
        ]
