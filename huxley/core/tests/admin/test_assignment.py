# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from contextlib import closing

from django.core.urlresolvers import reverse
from django.test import TestCase

from huxley.core.models import Assignment, Committee, Country, Registration, School
from huxley.utils.test import models, TestFiles


class AssignmentAdminTest(TestCase):

    fixtures = ['conference']

    def test_import(self):
        '''Test that the admin panel can import Assignments.'''
        models.new_superuser(username='testuser', password='test')
        self.client.login(username='testuser', password='test')

        registration = models.new_registration()
        cm1 = models.new_committee(name='SPD')
        cm2 = models.new_committee(name='USS')
        co1 = models.new_country(name="Côte d'Ivoire")
        co2 = models.new_country(name='Barbara Boxer')

        f = TestFiles.new_csv([
            ['Test School', 'SPD', "Côte d'Ivoire"],
            ['Test School', 'USS', 'Barbara Boxer']
        ])

        with closing(f) as f:
            self.client.post(reverse('admin:core_assignment_load'), {'csv': f})

        self.assertTrue(
            Assignment.objects.filter(
                registration=registration,
                committee=Committee.objects.get(name='SPD'),
                country=Country.objects.get(name="Côte d'Ivoire")).exists())
        self.assertTrue(
            Assignment.objects.filter(
                registration=registration,
                committee=Committee.objects.get(name='USS'),
                country=Country.objects.get(name='Barbara Boxer')).exists())

    def test_auto_assign(self):
        '''Test that the automated assignments obeys the proper rules for stable marriage.'''
        models.new_superuser(username='testuser', password='test')
        self.client.login(username='testuser', password='test')
        countries = [models.new_country(name='test_country_' + str(i))
                     for i in range(3)]
        normal_committees = [models.new_committee(
            name='normal_' + str(i), delegation_size=2) for i in range(20)]
        special_committees = [models.new_committee(
            name='special_' + str(i), delegation_size=1) for i in range(5)]
        assignments = []

        def add_free_assigment(assigments, committee, country):
            assignments.append(
                models.new_assignment(
                    committee=committee, country=country))
            assignments[-1].registration = None
            assignments[-1].save()

        for committee in normal_committees + special_committees:
            add_free_assigment(assignments, committee, countries[0])

        Registration.objects.all().delete()
        schools = [models.new_school(name='test_school_' + str(i))
                   for i in range(20)]
        registrations = [models.new_registration(
            school=schools[i], num_advanced_delegates=2) for i in range(3)]

        # Case 1: No conflicts. Every school gets their choice.
        committee_prefs = {}
        country_prefs = {}
        for i in range(len(registrations)):
            r = registrations[i]
            r.committee_preferences = Committee.objects.filter(
                name__in=['normal_' + str(i)])
            r.save()
            models.new_country_preference(
                registration=r, country=countries[0], rank=1)

            country_prefs[r] = countries[0]
            committee_prefs[r] = normal_committees[i]

        response_1 = self.client.get(reverse('admin:core_assignment_assign'))
        response_1_array = response_1.content.split("\r\n")
        header = ['School', 'Committee', 'Country', 'Rejected']
        fields_csv = ",".join(map(str, header)) + "\r\n"
        for r in registrations:
            for _ in range(committee_prefs[r].delegation_size):
                fields = [r.school.name, committee_prefs[r].name,
                          country_prefs[r].name, False]
                fields_csv += ','.join(map(str, fields)) + "\r\n"
        self.assertEquals(fields_csv, response_1.content)

        # Case 2: Conflicts; preference given in registration order.
        registrations_2 = [models.new_registration(
            school=schools[3 + i], num_advanced_delegates=2) for i in range(3)]
        for i in range(len(registrations_2)):
            r = registrations_2[i]
            r.committee_preferences = Committee.objects.filter(
                name__in=['normal_' + str(j)
                          for j in range(10)]).order_by('name')
            r.save()

            country_prefs[r] = countries[0]
            committee_prefs[r] = normal_committees[len(registrations_2) + i]

        response_2 = self.client.get(reverse('admin:core_assignment_assign'))
        response_2_array = response_2.content.split("\r\n")
        fields_csv_2 = ",".join(map(str, header)) + "\r\n"
        for r in registrations:
            for _ in range(committee_prefs[r].delegation_size):
                fields = [r.school.name, committee_prefs[r].name,
                          country_prefs[r].name, False]
                fields_csv_2 += ','.join(map(str, fields)) + "\r\n"

        for r in registrations_2:
            for _ in range(committee_prefs[r].delegation_size):
                fields = [r.school.name, committee_prefs[r].name,
                          country_prefs[r].name, False]
                fields_csv_2 += ','.join(map(str, fields)) + "\r\n"

        self.assertEquals(fields_csv_2, response_2.content)

        for item in response_1_array:
            self.assertTrue(item in response_2_array)

        # Case 3: Make sure odd number delegates are assigned to special committees and assignments are not overwritten.
        registrations_3 = [models.new_registration(
            school=schools[6 + i], num_advanced_delegates=3) for i in range(3)]
        assignments[0].registration = registrations_3[0]
        assignments[0].save()
        assignments[1].registration = registrations[-1]
        assignments[1].save()
        for i in range(len(registrations_3)):
            r = registrations_3[i]
            r.committee_preferences = Committee.objects.filter(
                name__in=['normal_' + str(j)
                          for j in range(6)]).order_by('name')
            r.save()

            country_prefs[r] = countries[0]
            committee_prefs[r] = normal_committees[i]

        response_3 = self.client.get(reverse('admin:core_assignment_assign'))
        response_3_array = response_3.content.split("\r\n")

        self.assertTrue(
            response_3.content.count('special') == len(registrations_3))
        self.assertTrue('{0},{1},{2},{3}'.format(
            registrations_3[0].school.name, assignments[0].committee.name,
            assignments[0].country.name, False) in response_3.content)
        self.assertTrue('{0},{1},{2},{3}'.format(
            registrations[-1].school.name, assignments[1].committee.name,
            assignments[1].country.name, False) in response_3.content)

        for committee in normal_committees + special_committees:
            for country in countries[1:]:
                add_free_assigment(assignments, committee, country)

        registrations_4 = [models.new_registration(
            school=schools[9 + i],
            num_intermediate_delegates=4,
            num_advanced_delegates=3) for i in range(3)]
        for i in range(len(registrations_4)):
            r = registrations_4[i]
            r.committee_preferences = Committee.objects.filter(
                name__in=['normal_' + str(j)
                          for j in range(6)]).order_by('name')
            r.save()

            country_prefs[r] = countries[0]
            committee_prefs[r] = normal_committees[i]

        # Case 4: Make sure that every registration gets the right number of assignments, that committees accept multiple schools
        response_4 = self.client.get(reverse('admin:core_assignment_assign'))
        response_4_array = response_4.content.split("\r\n")
        all_registrations = Registration.objects.all()
        total_delegates = sum(
            [r.num_beginner_delegates + r.num_intermediate_delegates +
             r.num_advanced_delegates for r in all_registrations])

        # CSV has two extra rows; header and empty final line
        self.assertTrue(len(response_4_array) == total_delegates + 2)
        self.assertTrue(
            response_4.content.count('{0}'.format(normal_committees[0].name))
            == 6)
