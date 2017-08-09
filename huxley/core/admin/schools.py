# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from huxley.core.models import School


class SchoolAdmin(admin.ModelAdmin):

    search_fields = ('name',)

    def calc_balance(self, obj):
        return obj.balance()

    def info(self, request):
        ''' Returns a CSV file containing the current set of
            Schools registered with all of its fields. '''
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
            "Waitlist",
            "Beginners",
            "Intermediates",
            "Advanced",
            "Spanish Speakers",
            "Chinese Speakers",
            "Registration Comments",
            "Fees Owed",
            "Fees Paid",
            "Modified At",
        ])

        for school in School.objects.all().order_by('name'):
            writer.writerow([unicode(field).encode('utf8')
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
                                 school.waitlist,
                                 school.beginner_delegates,
                                 school.intermediate_delegates,
                                 school.advanced_delegates,
                                 school.spanish_speaking_delegates,
                                 school.chinese_speaking_delegates,
                                 school.registration_comments,
                                 school.fees_owed,
                                 school.fees_paid,
                                 school.modified_at.isoformat(),
                             ]])

        return schools

    def preferences(self, request):
        ''' Returns a CSV file containing the current set of
            Schools registered with all of its fields. '''
        schools = HttpResponse(content_type='text/csv')
        schools[
            'Content-Disposition'] = 'attachment; filename="preferences.csv"'
        writer = csv.writer(schools)

        writer.writerow([
            "Name", "Assignments Requested", "Beginners", "Intermediates",
            "Advanced", "Spanish Speakers", "Chinese Speakers", "Country 1",
            "Country 2", "Country 3", "Country 4", "Country 5", "Country 6",
            "Country 7", "Country 8", "Country 9", "Country 10",
            "Committee Preferences", "Registration Comments"
        ])

        for school in School.objects.all().order_by('name'):
            countryprefs = [c
                            for c in school.countrypreferences.all().order_by(
                                'countrypreference')]
            countryprefs += [''] * (10 - len(countryprefs))
            committeeprefs = [', '.join(
                [c.name for c in school.committeepreferences.all()])]

            writer.writerow(
                [unicode(field).encode('utf8')
                 for field in [
                     school.name, school.beginner_delegates +
                     school.intermediate_delegates + school.advanced_delegates,
                     school.beginner_delegates, school.intermediate_delegates,
                     school.advanced_delegates,
                     school.spanish_speaking_delegates,
                     school.chinese_speaking_delegates
                 ]] + countryprefs + committeeprefs + [unicode(
                     school.registration_comments).encode('utf8')])

        return schools

    def get_urls(self):
        return super(SchoolAdmin, self).get_urls() + [
            url(r'info',
                self.admin_site.admin_view(self.info),
                name='core_school_info', ),
            url(r'preferences',
                self.admin_site.admin_view(self.preferences),
                name='core_school_preferences')]
