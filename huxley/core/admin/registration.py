# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from huxley.core.models import Registration


class RegistrationAdmin(admin.ModelAdmin):
    def info(self, request):
        '''Returns a CSV file of all the registration information.'''
        registrations = HttpResponse(content_type='text/csv')
        registrations[
            'Content-Disposition'] = 'attachment; filename="registration_info.csv"'

        writer = csv.writer(registrations)
        writer.writerow([
            "Registration Time", "School Name", "Total Number of Delegates",
            "Beginners", "Intermediates", "Advanced", "Spanish Speakers",
            "Chinese Speakers", "Assignments Finalized", "Waivers Complete", 
            "Delegate Fees Paid", "Delegate Fees Owed", "Paid Registration Fee?", 
            "Country 1", "Country 2", "Country 3", "Country 4", "Country 5", 
            "Country 6", "Country 7", "Country 8", "Country 9", "Country 10",
            "Committee Preferences", "Registration Comments"
        ])

        for registration in Registration.objects.all().order_by(
                'school__name'):
            country_preferences = [
                cp
                for cp in registration.country_preferences.all().order_by(
                    'countrypreference')
            ]
            country_preferences += [''] * (10 - len(country_preferences))
            committee_preferences = [', '.join(
                cp.name for cp in registration.committee_preferences.all())]

            writer.writerow(
                [unicode(field).encode('utf8')
                 for field in [
                     registration.registered_at,
                     registration.school.name,
                     registration.num_beginner_delegates +
                     registration.num_intermediate_delegates +
                     registration.num_advanced_delegates,
                     registration.num_beginner_delegates,
                     registration.num_intermediate_delegates,
                     registration.num_advanced_delegates,
                     registration.num_spanish_speaking_delegates,
                     registration.num_chinese_speaking_delegates,
                     registration.assignments_finalized,
                     registration.waivers_completed,
                     registration.delegate_fees_paid,
                     registration.delegate_fees_owed,
                     registration.registration_fee_paid
                 ]] + country_preferences + committee_preferences + [unicode(
                     registration.registration_comments).encode('utf8')])

        return registrations

    def get_urls(self):
        return super(RegistrationAdmin, self).get_urls() + [
            url(r'info',
                self.admin_site.admin_view(self.info),
                name='core_registration_info', )
        ]
