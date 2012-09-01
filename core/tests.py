"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
from core.models import *
from core.forms.registration import RegistrationForm


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

        params = self.valid_params.copy()

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
        params = self.valid_params.copy()
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
        params = self.valid_params.copy()
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


    def test_create_user(self):
        """ Tests parameters and db insertion """

        params = self.valid_params.copy()
        params["Username"] = "ajummaTaeng"
        form = RegistrationForm(params)

        self.assertTrue(form.is_valid())
        user = form.create_user()

        # Check return value
        self.assertEqual(user.username, params["Username"])
        self.assertEqual(user.first_name, params["FirstName"])
        self.assertEqual(user.last_name, params["LastName"])

        # Check to see that it's in the database as well
        users_in_db = User.objects.filter(username=params["Username"])
        self.assertGreater(len(users_in_db), 0)
        self.assertEqual(users_in_db[0], user)


    def test_username_unique(self):
        """ Tests for: uniqueness """
        
        params = self.valid_params.copy()
        params["Username"] = "abcdef"

        # This should be valid, as "abcdef" should be unique
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())
        form.create_user()

        # Try again and it should throw a validation error
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("Username", form.errors)
        self.assertItemsEqual(form.errors["Username"], ["Username '%s' is already in use. Please choose another one." % (params["Username"])])


    def test_password_len(self):
        """ Tests for: minimum length """
        params = self.valid_params.copy()
        # Tests len < 6
        params["Password"] = "abcde"
        params["Password2"] = "abcde"

        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("Password", form.errors)
        self.assertItemsEqual(form.errors["Password"], ["Ensure this value has at least 6 characters (it has 5)."])

        # Tests len == 6
        params["Password"] = "abcdef"
        params["Password2"] = "abcdef"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Tests len > 6
        params["Password"] = "abcdefgh"
        params["Password2"] = "abcdefgh"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_password_confirm(self):
        """ Tests that password and password2 match """

        params = self.valid_params.copy()
        params["Password"] = "abcdef"
        params["Password2"] = "abcdefg"

        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 2)
        self.assertIn("Password", form.errors)
        self.assertIn("Password2", form.errors)
        self.assertItemsEqual(form.errors["Password"], ["Passwords do not match!"])
        self.assertItemsEqual(form.errors["Password2"], ["Passwords do not match!"])


    def test_password_chars(self):
        """ Tests that password contains only valid characters (alphanumeric, underscore, ., symbols on number keys) """
        # Invalid characters
        params = self.valid_params.copy()
        params["Password"] = "~[]\[]]\[]\[\]"
        params["Password2"] = "~[]\[]]\[]\[\]"

        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("Password", form.errors)
        self.assertItemsEqual(form.errors["Password"], ["Password contains invalid characters."])

        # Valid characters
        params["Password"] = "abcdefg!@#$%^&*"
        params["Password2"] = "abcdefg!@#$%^&*"

        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_create_school(self):
        """ Tests that the form creates a school object in the DB properly """

        # Test that American schools are created properly
        params = self.valid_params.copy()
        params["SchoolName"] = "GirlsGeneration"

        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        school = form.create_school()
        self.assertFalse(school is None)

        self.assertEqual(school.name, params["SchoolName"])
        self.assertEqual(school.address, params["SchoolAddress"])
        self.assertEqual(school.city, params["SchoolCity"])
        self.assertEqual(school.state, params["SchoolState"])
        self.assertEqual(school.zip, str(params["SchoolZip"]))
        self.assertEqual(school.primaryname, params["PrimaryName"])
        self.assertEqual(school.primaryemail, params["PrimaryEmail"])
        self.assertEqual(school.primaryphone, params["PrimaryPhone"])
        self.assertEqual(school.programtype, params["programtype"])
        self.assertEqual(school.timesattended, params["howmany"])
        self.assertEqual(school.mindelegationsize, params["MinDelegation"])
        self.assertEqual(school.maxdelegationsize, params["MaxDelegation"])
        self.assertFalse(school.international)

        if "SecondaryName" in params:
            self.assertEqual(school.secondaryname, params["SecondaryName"])
        if "SecondaryEmail" in params:
            self.assertEqual(school.secondaryemail, params["SecondaryEmail"])
        if "SecondaryPhone" in params:
            self.assertEqual(school.secondaryphone, params["SecondaryPhone"])

        # Check to see that it's in the database as well
        schools_in_db = School.objects.filter(name=params["SchoolName"])
        self.assertGreater(len(schools_in_db), 0)
        self.assertEqual(schools_in_db[0], school)

        # Test international school creation
        params["SchoolName"] = "GirlsGenerationInternational"
        params["SchoolCountry"] = 10
        params["us_or_int"] = "international"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        school = form.create_school()
        self.assertFalse(school is None)
        self.assertEqual(school.name, params["SchoolName"])
        self.assertEqual(school.address, params["SchoolAddress"])
        self.assertEqual(school.city, params["SchoolCity"])
        self.assertEqual(school.state, params["SchoolState"])
        self.assertEqual(school.zip, str(params["SchoolZip"]))
        self.assertEqual(school.primaryname, params["PrimaryName"])
        self.assertEqual(school.primaryemail, params["PrimaryEmail"])
        self.assertEqual(school.primaryphone, params["PrimaryPhone"])
        self.assertEqual(school.programtype, params["programtype"])
        self.assertEqual(school.timesattended, params["howmany"])
        self.assertEqual(school.mindelegationsize, params["MinDelegation"])
        self.assertEqual(school.maxdelegationsize, params["MaxDelegation"])
        self.assertTrue(school.international)

        if "SecondaryName" in params:
            self.assertEqual(school.secondaryname, params["SecondaryName"])
        if "SecondaryEmail" in params:
            self.assertEqual(school.secondaryemail, params["SecondaryEmail"])
        if "SecondaryPhone" in params:
            self.assertEqual(school.secondaryphone, params["SecondaryPhone"])

        # Check to see that it's in the database as well
        schools_in_db = School.objects.filter(name=params["SchoolName"])
        self.assertGreater(len(schools_in_db), 0)
        self.assertEqual(schools_in_db[0], school)


    def test_school_uniqueness(self):
        """ Tests that the school name checks if it's unique """
        params = self.valid_params.copy()
        params["SchoolName"] = "MySchool"

        # This should be valid, as "abcdef" should be unique
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())
        form.create_school()

        # This shouldn't be valid.
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("SchoolName", form.errors)
        self.assertItemsEqual(form.errors["SchoolName"], ["A school with the name '%s' has already been registered." % (params["SchoolName"])])

        # Now try another valid one
        params["SchoolName"] = "MySchool2"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())


    def test_add_country_preferences(self):
        """ Tests that adding country preferences works """
        # Initialization
        params = self.valid_params.copy()
        for i in xrange(1,11):
            params["CountryPref" + str(i)] = 0

        # No preferences at all
        params["SchoolName"] = "CountryTest1"
        form = RegistrationForm(params)

        self.assertTrue(form.is_valid())
        school = form.create_school()
        self.assertTrue(form.add_country_preferences(school))

        prefs = CountryPreference.objects.filter(school=school)
        self.assertEqual(len(prefs), 0)

        # Couple of random preferences scattered around
        params["SchoolName"] = "CountryTest2"
        params["CountryPref1"] = 2
        params["CountryPref3"] = 10
        params["CountryPref7"] = 7
        form = RegistrationForm(params)

        self.assertTrue(form.is_valid())
        school = form.create_school()
        self.assertTrue(form.add_country_preferences(school))

        prefs = CountryPreference.objects.filter(school=school)
        self.assertEqual(len(prefs), 3)

        for pref in prefs:
            self.assertIn(pref.rank, (1,2,3))
            if pref.rank == 1:
                self.assertEqual(pref.country.id, params["CountryPref1"])
            elif pref.rank == 2:
                self.assertEqual(pref.country.id, params["CountryPref3"])
            elif pref.rank == 3:
                self.assertEqual(pref.country.id, params["CountryPref7"])
            else:
                self.assertTrue(False)


    def test_country_preferences(self):
        """ Tests that country preferences are optional """
        # Initialization
        params = self.valid_params.copy()
        for i in xrange(1,11):
            params["CountryPref" + str(i)] = 0

        # Should be valid even with no country preferences
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Couple of unique country preferences; valid
        params["CountryPref1"] = 1
        params["CountryPref3"] = 10
        params["CountryPref7"] = 7

        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        
    def test_add_committee_preferences(self):
        """ Tests that adding committee preferences works """
        params = self.valid_params.copy()
        params["SchoolName"] = "CommitteeTest1"
        form = RegistrationForm(params)

        # No committee preferences
        self.assertTrue(form.is_valid())
        school = form.create_school()
        self.assertTrue(form.add_committee_preferences(school))
        self.assertEqual(len(school.committeepreferences.all()), 0)

        # Some preferences
        params["CommitteePrefs"] = [13, 14, 19]
        params["SchoolName"] = "CommitteeTest2"
        form = RegistrationForm(params)

        self.assertTrue(form.is_valid())
        school = form.create_school()
        self.assertTrue(form.add_committee_preferences(school))
        self.assertEqual(len(school.committeepreferences.all()), 3)

        for committee in school.committeepreferences.all():
            self.assertIn(committee.id, params["CommitteePrefs"])


    def test_create_advisor_profile(self):
        """ Tests that an advisor profile for a user and a school is successfully created upon registration """
        params = self.valid_params.copy()
        params["Username"] = "advisor_profile_test"
        params["SchoolName"] = "advisor_profile_test"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        user = form.create_user()
        school = form.create_school()

        profile = form.create_advisor_profile(user, school)
        self.assertFalse(profile is None)

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.school, school)


    def test_us_phone_nums(self):
        """ Tests the US phone number validation code """
        params = self.valid_params.copy()
        params["us_or_int"] = "us"

        # (XXX) XXX-XXXX
        params["PrimaryPhone"] = "(123) 456-7890"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # (XXX) XXX-XXXX xXXXX (extension)
        params["PrimaryPhone"] = "(123) 456-7890 x1234"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # 123-456-7890 (invalid)
        params["PrimaryPhone"] = "123-456-7890"
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("PrimaryPhone", form.errors)
        self.assertItemsEqual(form.errors["PrimaryPhone"], ["Phone in incorrect format."])
        
        # (123) 12a-1231 (invalid)
        params["PrimaryPhone"] = "(123) 12a-1231"
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("PrimaryPhone", form.errors)
        self.assertItemsEqual(form.errors["PrimaryPhone"], ["Phone in incorrect format."])


    def test_international_phone_nums(self):
        """ Tests the international phone number validation code """
        params = self.valid_params.copy()
        params["us_or_int"] = "international"
        params["SchoolCountry"] = "Japan"

        # 1234534653465 (just numbers; valid)
        params["PrimaryPhone"] = "123434645657"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # 1-123-123-1234 (dashes; valid)
        params["PrimaryPhone"] = "1-123-123-1234"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())        

        # US format (valid)
        params["PrimaryPhone"] = "(123) 456-7890"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # US format with invalid characters
        params["PrimaryPhone"] = "(12a) 456-7890"
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("PrimaryPhone", form.errors)
        self.assertItemsEqual(form.errors["PrimaryPhone"], ["Phone in incorrect format."])

        # Numbers with invalid characters
        params["PrimaryPhone"] = "1-234-4a3-as,f"
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("PrimaryPhone", form.errors)
        self.assertItemsEqual(form.errors["PrimaryPhone"], ["Phone in incorrect format."])


    def test_school_country(self):
        """ Tests that school country is filled out when it's an international school """
        params = self.valid_params.copy()
        
        # Try US first (no country specified)
        params["us_or_int"] = "us"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Try US with a country (shouldn't matter)
        params["SchoolCountry"] = "America"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

        # Try international (with no country specified)
        params = self.valid_params.copy() 
        params["us_or_int"] = "international"
        form = RegistrationForm(params)
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors), 1)
        self.assertIn("SchoolCountry", form.errors)
        self.assertItemsEqual(form.errors["SchoolCountry"], ["You must specify a country."])

        # Try international (with a country)
        params["SchoolCountry"] = "Japan"
        form = RegistrationForm(params)
        self.assertTrue(form.is_valid())

