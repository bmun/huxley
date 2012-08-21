"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
from cms.models import *
from cms.forms.registration import RegistrationForm


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}


class RegistrationTest(unittest.TestCase):

    optional_fields = ("SchoolCountry", "SecondaryName", "SecondaryEmail", "SecondaryPhone", "CommitteePrefs", "CountryPref1", "CountryPref2", "CountryPref3", "CountryPref4", "CountryPref5", "CountryPref6", "CountryPref7", "CountryPref8", "CountryPref9", "CountryPref10")

    def test_sanity(self):
        """ Simple test case that makes sure a form with all valid data works """

        params = {"FirstName": "Taeyeon", "LastName": "Kim", 
                  "Username": "taengoo", "Password": "girlsgeneration", 
                  "Password2": "girlsgeneration", "us_or_int":"us",
                  "SchoolName": "SNSD", "SchoolAddress": "123 SNSD Way",
                  "SchoolCity": "Seoul", "SchoolState": "Seoul",
                  "SchoolZip":12345, "programtype": "club", 
                  "howmany":9, "MinDelegation":9, "MaxDelegation":9,
                  "PrimaryName":"Manager", "PrimaryEmail":"kimtaeyon@snsd.com",
                  "PrimaryPhone":"(123) 435-7543", "CountryPref1": "South Korea",
                  "CountryPref2": "China", "CountryPref3": "United States", 
                  "CountryPref4": "United Kingdom", "CountryPref5": "France",
                  "CountryPref6": "Spain", "CountryPref7": "Japan", 
                  "CountryPref8": "Italy", "CountryPref9": "Germany",
                  "CountryPref10": "Russia"}

        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_required(self):
        """ Simple test case to make sure all fields except for the optional ones are required """

        params = {"FirstName":""} # Empty string is not valid
        form = RegistrationForm(params)

        valid = form.is_valid()
        self.assertFalse(valid)

        # Check that all required fields are in form.errors.
        for field in form.cleaned_data:
            if field not in self.optional_fields:
                self.assertIn(field, form.errors)


    # def test_valid_usernames(self):
    #     pass