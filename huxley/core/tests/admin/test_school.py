# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.utils.test import TestSchools, TestUsers


class SchoolAdminTest(TestCase):

    def test_info_export(self):
        '''Test that the admin panel can properly export a list of schools.'''
        TestUsers.new_user(username='testuser1', password='test1')
        TestUsers.new_superuser(username='testuser2', password='test2')
        self.client.login(username='testuser1', password='test1')
        school = TestSchools.new_school()
        self.client.logout()
        self.client.login(username='testuser2', password='test2')

        response = self.client.get(reverse('admin:core_school_info'))

        self.assertTrue(response)

        header = [
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
            "Bilingual?",
            "Specialized/Regional?",
            "Crisis?",
            "Alternative?",
            "Press Corps?",
            "Registration Comments",
            "Fees Owed",
            "Fees Paid",
        ]

        fields_csv = ",".join(map(str, header)) + "\r\n"

        fields = [
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
            school.prefers_bilingual,
            school.prefers_specialized_regional,
            school.prefers_crisis,
            school.prefers_alternative,
            school.prefers_press_corps,
            school.registration_comments,
            int(school.fees_owed),
            int(school.fees_paid),
        ]

        fields_csv += ",".join(map(str, fields))
        self.assertEquals(fields_csv, response.content[:-2])

    def test_preference_export(self):
        '''Test that the admin panel can properly export school preferences.'''
        TestUsers.new_user(username='testuser1', password='test1')
        TestUsers.new_superuser(username='testuser2', password='test2')
        self.client.login(username='testuser1', password='test1')
        school = TestSchools.new_school()
        self.client.logout()
        self.client.login(username='testuser2', password='test2')

        response = self.client.get(reverse('admin:core_school_preferences'))

        self.assertTrue(response)

        header = [
            "Name",
            "Assignments Requested",
            "Beginners",
            "Intermediates",
            "Advanced",
            "Spanish Speakers",
            "Bilingual?",
            "Specialized/Regional?",
            "Crisis?",
            "Alternative?",
            "Press Corps?",
            "Country 1",
            "Country 2",
            "Country 3",
            "Country 4",
            "Country 5",
            "Country 6",
            "Country 7",
            "Country 8",
            "Country 9",
            "Country 10",
            "Registration Comments"
            ]

        fields_csv = ",".join(map(str, header)) + "\r\n"

        countryprefs = [c for c in school.countrypreferences.all()]
        countryprefs += [''] * (10 - len(countryprefs))

        fields = [
                school.name,
                school.beginner_delegates + school.intermediate_delegates + school.advanced_delegates,
                school.beginner_delegates,
                school.intermediate_delegates,
                school.advanced_delegates,
                school.spanish_speaking_delegates,
                school.prefers_bilingual,
                school.prefers_specialized_regional,
                school.prefers_crisis,
                school.prefers_alternative,
                school.prefers_press_corps]
        fields.extend(countryprefs)
        fields.append(school.registration_comments)

        fields_csv += ",".join(map(str, fields))
        self.assertEquals(fields_csv, response.content[:-2])
