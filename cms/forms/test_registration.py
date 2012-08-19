from django.utils import unittest
from cms.forms.registration import RegistrationForm


class RegistrationTest(unittest.TestCase):

    optional_fields = ("SchoolCountry", "SecondaryName", "SecondaryEmail", "SecondaryPhone", "CommitteePrefs")


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
        assertTrue(form.is_valid())


    def test_required(self):
        """ Simple test case to make sure all fields except for the optional ones are required """

        params = {"FirstName":""} # Empty string is not valid
        form = RegistrationForm(params)

        valid = form.is_valid()
        assertFalse(valid)

        # Check that all required fields are in form.errors.
        for field in form.cleaned_data:
            if field not in self.optional_fields:
                assertIn(field, form.errors)


    def test_valid_usernames(self):
        pass