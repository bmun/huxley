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

    valid_params = {"FirstName": "Taeyeon", "LastName": "Kim", 
                    "Username": "taengoo", "Password": "girlsgeneration", 
                    "Password2": "girlsgeneration", "us_or_int":"us",
                    "SchoolName": "SNSD", "SchoolAddress": "123 SNSD Way",
                    "SchoolCity": "Seoul", "SchoolState": "Seoul",
                    "SchoolZip":12345, "programtype": "club", 
                    "howmany":9, "MinDelegation":9, "MaxDelegation":9,
                    "PrimaryName":"Manager", "PrimaryEmail":"kimtaeyon@snsd.com",
                    "PrimaryPhone":"(123) 435-7543", "CountryPref1": 1,
                    "CountryPref2": 2, "CountryPref3": 3, 
                    "CountryPref4": 4, "CountryPref5": 5,
                    "CountryPref6": 6, "CountryPref7": 7, 
                    "CountryPref8": 8, "CountryPref9": 9,
                    "CountryPref10": 10}

    def test_sanity(self):
        """ Simple test case that makes sure a form with all valid data works """

        params = self.valid_params

        form = RegistrationForm(params)
        if not form.is_valid():
            print "----- Test: test_sanity ----------------------------------------------------------------------------"
            for name, errors in form.errors.items():
                for error in errors:
                    print "> [Field: %s] Validation Error: %s" % (name, error)
            print "----------------------------------------------------------------------------------------------------"
        self.assertTrue(form.is_valid())


    def test_required(self):
        """ Simple test case to make sure all fields except for the optional ones are required """

        params = {"FirstName":""} # Empty string is not valid
        form = RegistrationForm(params)

        valid = form.is_valid()
        self.assertFalse(valid)

        # Check that all required fields are in form.errors.
        for name, field in form.fields.items():
            if field.required:
                self.assertIn(name, form.errors)
            else:
                self.assertNotIn(name, form.errors)


    def test_username_len(self):
        """ Tests for: minimum length """

        # Too short (len: 3)
        params = self.valid_params
        params["Username"] = "abc" # Too short, so invalid

        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("Username", form.errors)
        # Make sure it's the only error (i.e. no other validation errors for usernames)
        self.assertItemsEqual(form.errors["Username"], ["Ensure this value has at least 4 characters (it has 3)."])

        # Valid username, since it's at least 4 characters long
        params["Username"] = "abcd"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Valid username, since it's at least 4 characters long
        params["Username"] = "abcdesdfdsfasdf"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_username_chars(self):
        """ Tests for: valid characters (alphanumeric, hyphens, underscores) """

        # All invalid characters
        params = self.valid_params
        params["Username"] = "!@#$"
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("Username", form.errors)
        self.assertItemsEqual(form.errors["Username"], ["Usernames must be alphanumeric, underscores, and/or hyphens only."])

        # Mixture of valid and invalid characters
        params["Username"] = "abc!defgh"
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("Username", form.errors)
        self.assertItemsEqual(form.errors["Username"], ["Usernames must be alphanumeric, underscores, and/or hyphens only."])

        # Looks valid but isn't
        params["Username"] = "Rick Astley"
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("Username", form.errors)
        self.assertItemsEqual(form.errors["Username"], ["Usernames must be alphanumeric, underscores, and/or hyphens only."])        

        # Just valid characters
        params["Username"] = "RickAstley"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_username_unique(self):
        """ Tests for: uniqueness """
        pass

