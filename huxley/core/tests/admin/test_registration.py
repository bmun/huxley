# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.utils.test import models


class RegistrationAdminTest(TestCase):

    fixtures = ['conference']

    def test_preference_export(self):
        '''Tests that the admin panel can export registration data.'''
        registration = models.new_registration()

        models.new_superuser(username='superuser', password='superuser')
        self.client.login(username='superuser', password='superuser')

        response = self.client.get(reverse('admin:core_registration_info'))

        header = [
            "Registration Time", "School Name", "Total Number of Delegates",
            "Beginners", "Intermediates", "Advanced", "Spanish Speakers",
            "Chinese Speakers",  "Assignments Finalized", "Waivers Complete", 
            "Delegate Fees Paid", "Delegate Fees Owed", "Paid Registration Fee?", 
            "Country 1", "Country 2", "Country 3", "Country 4", "Country 5", 
            "Country 6", "Country 7", "Country 8", "Country 9", "Country 10", 
            "Committee Preferences", "Registration Comments"
        ]

        fields_csv = ",".join(map(str, header)) + "\r\n"

        country_preferences = [cp
                               for cp in registration.country_preferences.all(
                               ).order_by('countrypreference')]
        country_preferences += [''] * (10 - len(country_preferences))
        committee_preferences = [', '.join(
            cp.name for cp in registration.committee_preferences.all())]

        fields = [
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
        ]
        fields.extend(country_preferences)
        fields.extend(committee_preferences)
        fields.extend(registration.registration_comments)

        fields_csv += ','.join(map(str, fields))
        self.assertEquals(fields_csv, response.content[:-3])
