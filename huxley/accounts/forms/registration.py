# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django import forms
from django.contrib.auth.models import User

from huxley.core.models import *

from datetime import date
import re

countries = Country.objects.filter(special=False).order_by('name')
country_choices = [(country.id, country.name) for country in countries]
country_choices.insert(0, (0, "No Preference"))

special_committees = Committee.objects.filter(special=True).order_by('full_name')
special_committees_choices = [(committee.id, committee.full_name) for committee in special_committees]

class RegistrationForm(forms.Form):
    # By default, fields are required unless you specify required=False

    # User Information
    FirstName = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class':'half required'}))
    LastName = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class':'half required'}))
    Username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'third required uniqueUser username'}), min_length=4)
    Password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'third required pass1 validChars'}), min_length=6)
    Password2 = forms.CharField(label="Password (again)", widget=forms.PasswordInput(attrs={'class':'third required pass1 validChars'}))

    # School Information
    us_or_int = forms.ChoiceField(label="Where is your school?", widget=forms.RadioSelect(attrs={'class':'int_check', 'name':'us_or_int'}), choices=(('us', 'United States'), ('international', 'International')), initial="us")
    SchoolName = forms.CharField(label="Official School Name", widget=forms.TextInput(attrs={'class':'full required'}))
    SchoolAddress = forms.CharField(label="Address", widget=forms.TextInput(attrs={'class':'full required'}))
    SchoolCity = forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'third required'}))
    SchoolState = forms.CharField(label="State", widget=forms.TextInput(attrs={'class':'third required'}), required=False)
    SchoolZip = forms.CharField(label="Zip", widget=forms.TextInput(attrs={'class':'third required zip'}), min_length=5)
    SchoolCountry = forms.CharField(label="Country", widget=forms.TextInput(attrs={'class':'showhide'}), required=False)

    # Program Information
    program_type = forms.ChoiceField(label="What category best describes your program?", widget=forms.RadioSelect, choices=School.PROGRAM_TYPE_OPTIONS, initial=School.TYPE_CLUB)
    howmany = forms.IntegerField(label="# of BMUN Sessions Attended", widget=forms.TextInput(attrs={'class':'third required IntegersOnly'}))
    MinDelegation = forms.IntegerField(label="Min. Delegation Size", widget=forms.TextInput(attrs={'class':'third required IntegersOnly'}))
    MaxDelegation = forms.IntegerField(label="Max. Delegation Size", widget=forms.TextInput(attrs={'class':'third required IntegersOnly'}))

    # Contact Information
    PrimaryName = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'third required'}))
    PrimaryEmail = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'third required email'}))
    PrimaryPhone = forms.CharField(label="Phone", widget=forms.TextInput(attrs={'class':'third required phoneNum phoneVal'}))
    SecondaryName = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'third'}), required=False)
    SecondaryEmail = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'third email'}), required=False)
    SecondaryPhone = forms.CharField(label="Phone", widget=forms.TextInput(attrs={'class':'third phoneNum phoneVal'}), required=False)

    # Country Preferences (the ids)
    CountryPref1 = forms.ChoiceField(label="01", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    CountryPref2 = forms.ChoiceField(label="02", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    CountryPref3 = forms.ChoiceField(label="03", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    CountryPref4 = forms.ChoiceField(label="04", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    CountryPref5 = forms.ChoiceField(label="05", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    CountryPref6 = forms.ChoiceField(label="06", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    CountryPref7 = forms.ChoiceField(label="07", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    CountryPref8 = forms.ChoiceField(label="08", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    CountryPref9 = forms.ChoiceField(label="09", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    CountryPref10 = forms.ChoiceField(label="10", widget=forms.Select(), choices=country_choices, required=False, initial=0)

    # Committee Preferences
    CommitteePrefs = forms.MultipleChoiceField(label="Special Committee Preferences", 
                                               widget=forms.CheckboxSelectMultiple(),
                                               choices=special_committees_choices,
                                               required=False)

    # ===== DB Functions ====================================================================
    # Run these only if the form is valid.
    
    def create_user(self):
        try:
            new_user = User.objects.create_user(self.cleaned_data['Username'], self.cleaned_data['PrimaryEmail'], self.cleaned_data['Password'])
            new_user.first_name = self.cleaned_data['FirstName']
            new_user.last_name = self.cleaned_data['LastName']
            new_user.save()
            return new_user
        except:
            print "> ERROR WHILE CREATING USER. REMEMBER TO VALIDATE FIRST."
            return None


    def create_school(self):
        registration_fee = 40.00 if date.today() < date(2012, 10, 20) else 50.00
        new_school = School.objects.create(name=self.cleaned_data['SchoolName'],
                                           address=self.cleaned_data['SchoolAddress'],
                                           city=self.cleaned_data['SchoolCity'],
                                           state=self.cleaned_data['SchoolState'],
                                           zip_code=self.cleaned_data['SchoolZip'],
                                           primary_name = self.cleaned_data['PrimaryName'],
                                           primary_email = self.cleaned_data['PrimaryEmail'],
                                           primary_phone = self.cleaned_data['PrimaryPhone'],
                                           secondary_name = self.cleaned_data['SecondaryName'],
                                           secondary_email = self.cleaned_data['SecondaryEmail'],
                                           secondary_phone = self.cleaned_data['SecondaryPhone'],
                                           program_type = int(self.cleaned_data['program_type']),
                                           times_attended = self.cleaned_data['howmany'],
                                           min_delegation_size = self.cleaned_data['MinDelegation'],
                                           max_delegation_size = self.cleaned_data['MaxDelegation'],
                                           international = self.cleaned_data['us_or_int'] == 'international',
                                           registration_fee = registration_fee)
        new_school.save()
        return new_school

    def add_country_preferences(self, school):
        country_ids = [int(self.cleaned_data['CountryPref%d' % i]) for i in xrange(1, 11)]
        school.refresh_country_preferences(country_ids)
        return True

    def add_committee_preferences(self, school):
        committee_ids = self.cleaned_data["CommitteePrefs"]
        school.refresh_committee_preferences(committee_ids)
        return True

    def create_advisor_profile(self, user, school):
        try:
            new_profile = AdvisorProfile.objects.create(user=user, school=school)
            new_profile.save()
            return new_profile
        except:
            print "> ERROR WHILE MAKING ADVISOR PROFILE."
            return None


    # ===== Validation ===============================================================================
    # Format: clean_<field>
    def clean_SchoolName(self):
        # Check for uniqueness
        school_name = self.cleaned_data['SchoolName']
        school_exists = School.objects.filter(name = school_name).exists()
        if school_exists:
            raise forms.ValidationError("A school with the name '%s' has already been registered." % (school_name))
        # Return data, whether changed or not
        return school_name


    def clean_Username(self):
        # Check for uniqueness
        username = self.cleaned_data['Username']
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            raise forms.ValidationError("Username '%s' is already in use. Please choose another one." % (username))
        # Make sure the characters are valid
        if re.match("^[A-Za-z0-9\_\-]+$", username) is None:
            raise forms.ValidationError("Usernames must be alphanumeric, underscores, and/or hyphens only.")
        # Return data, changed or not
        return username


    def clean_Password(self):
        password = self.cleaned_data['Password']
        if re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", password) is None:
            raise forms.ValidationError("Password contains invalid characters.") # TODO: make error message more informative
        # Return data, changed or not
        return password


    def phone_num_is_valid(self, number, international):
        if international == "international":
            if re.match("^[0-9\-x\s\+\(\)]+$", number):
                return True
            else:
                return False
        else:
            # Format: (123) 456-7890 || Note the space after the area code.
            if re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", number):
                return True
            else:
                return False


    # General clean method
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        Password = cleaned_data.get('Password')
        Password2 = cleaned_data.get('Password2')
        international = cleaned_data.get('us_or_int', 'us')
        primary_phone = cleaned_data.get('PrimaryPhone')
        secondary_phone = cleaned_data.get('SecondaryPhone')
        state = cleaned_data.get('SchoolState')
        country = cleaned_data.get('SchoolCountry')

        # Check to see if passwords match
        if Password and Password2 and Password != Password2:
            message = "Passwords do not match!"
            self._errors["Password"] = self.error_class([message])
            self._errors["Password2"] = self.error_class([message])
            # These fields are not valid anymore, so delete them from cleaned_data
            del cleaned_data["Password"]
            del cleaned_data["Password2"]

        # Check to see if the state is required
        if not state and international == "us":
            message = "This field is required."
            self._errors["SchoolState"] = self.error_class([message])
            del cleaned_data["SchoolState"]

        # Check to make sure phone number is formatted correctly
        if primary_phone and not self.phone_num_is_valid(primary_phone, international):
            message = "Phone in incorrect format."
            self._errors["PrimaryPhone"] = self.error_class([message])
            del cleaned_data["PrimaryPhone"]

        # Check to make sure phone number is formatted correctly
        if secondary_phone and not self.phone_num_is_valid(secondary_phone, international):
            message = "Phone in incorrect format."
            self._errors["SecondaryPhone"] = self.error_class([message])
            del cleaned_data["SecondaryPhone"]

        # Check to make sure a country is specified for international schools
        if international == "international":
            if not country or re.match("^\s*$", country) is not None:
                message = "You must specify a country."
                self._errors["SchoolCountry"] = self.error_class([message])
                
        # Always return cleaned_data
        return cleaned_data

