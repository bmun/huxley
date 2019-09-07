# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.urls import reverse
from django.test import TestCase

from huxley.utils.test import models


class SchoolAdminTest(TestCase):

    fixtures = ['conference']

    def test_info_export(self):
        '''Test that the admin panel can properly export a list of schools.'''
        models.new_user(username='testuser1', password='test1')
        models.new_superuser(username='testuser2', password='test2')
        self.client.login(username='testuser1', password='test1')
        school = models.new_school()
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
        ]

        fields_csv += ",".join(map(str, fields))
        self.assertEquals(fields_csv, response.content[:-2])
