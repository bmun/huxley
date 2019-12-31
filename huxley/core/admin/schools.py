# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from huxley.core.models import School


class SchoolAdmin(admin.ModelAdmin):

    search_fields = ('name', )

    def info(self, request):
        ''' Returns a CSV file containing the current set of
            Schools in our database with all of its fields. '''
        schools = HttpResponse(content_type='text/csv')
        schools['Content-Disposition'] = 'attachment; filename="schools.csv"'
        writer = csv.writer(schools)

        writer.writerow([
            "ID",
            "Name",
            "Address",
            "City",
            "State",
            "Zip Code",
            "Country",
            "Primary Name",
            "Primary Gender",
            "Primary Email",
            "Primary Phone",
            "Primary Type",
            "Secondary Name",
            "Secondary Gender",
            "Secondary Email",
            "Secondary Phone",
            "Secondary Type",
            "Program Type",
            "Times Attended",
            "International",
        ])

        for school in School.objects.all().order_by('name'):
            writer.writerow([str(field)
                             for field in [
                                 school.id,
                                 school.name,
                                 school.address,
                                 school.city,
                                 school.state,
                                 school.zip_code,
                                 school.country,
                                 school.primary_name,
                                 school.primary_gender,
                                 school.primary_email,
                                 school.primary_phone,
                                 school.primary_type,
                                 school.secondary_name,
                                 school.secondary_gender,
                                 school.secondary_email,
                                 school.secondary_phone,
                                 school.secondary_type,
                                 school.program_type,
                                 school.times_attended,
                                 school.international,
                             ]])

        return schools

    def get_urls(self):
        return super(SchoolAdmin, self).get_urls() + [
            url(r'info',
                self.admin_site.admin_view(self.info),
                name='core_school_info', )
        ]
