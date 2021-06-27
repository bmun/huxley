# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.utils import html

from huxley.core.models import Country


class CountryAdmin(admin.ModelAdmin):

    search_fields = ('name', )

    def load(self, request):
        '''Import a CSV file containing countries.'''
        countries = request.FILES
        reader = csv.reader(countries['csv'].read().decode('utf-8').splitlines())
        failed = []
        for row in reader:
            special = False if row[1].strip() == '0' or row[1].strip() == 'False' or not row[1] else True
            c = Country(name=row[0], special=special)
            try:
                c.save()
            except IntegrityError as e:
                failed.append(row[0])
        
        if failed:
            messages.error(
                    request,
                    html.format_html(
                        'The following countries failed to be uploaded. They might be duplicates. <br/>'
                        + '<br/>'.join(failed)))

        return HttpResponseRedirect(reverse('admin:core_country_changelist'))

    def get_urls(self):
        return super(CountryAdmin, self).get_urls() + [
            url(r'load',
                self.admin_site.admin_view(self.load),
                name='core_country_load'),
        ]
