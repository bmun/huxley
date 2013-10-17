# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from datetime import date
from django import forms

from huxley.accounts.models import HuxleyUser
from huxley.core.models import *

import re

countries = Country.objects.filter(special=False).order_by('name')
country_choices = [(country.id, country.name) for country in countries]
country_choices.insert(0, (0, "No Preference"))

special_committees = Committee.objects.filter(special=True).order_by('full_name')
special_committees_choices = [(committee.id, committee.full_name) for committee in special_committees]

class RegistrationForm(forms.Form):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'placeholder': 'First Name'}), label="First Name")
    last_name  = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'placeholder': 'Last Name'}), label="Last Name")
    username   = forms.CharField(widget=forms.TextInput(attrs={'class':'required uniqueUser username', 'placeholder': 'Username'}), min_length=4, label="Username")
    password   = forms.CharField(widget=forms.PasswordInput(attrs={'class':'required pass1 validChars', 'placeholder': 'Password'}), min_length=6, label="Password")
    password2  = forms.CharField(widget=forms.PasswordInput(attrs={'class':'required pass1 validChars', 'placeholder': 'Password (confirm)'}), label="Password (confirm)")

    school_location = forms.ChoiceField(label="Where is your school located?", widget=forms.RadioSelect(attrs={'class':'international-check', 'name':'school_location'}), choices=School.LOCATION_OPTIONS, initial=School.LOCATION_USA)
    school_name     = forms.CharField(label="Official School Name", widget=forms.TextInput(attrs={'class':'required', 'placeholder': 'Official School Name'}))
    school_address  = forms.CharField(label="Address", widget=forms.TextInput(attrs={'class':'required', 'placeholder': 'Street Address'}))
    school_city     = forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'required', 'placeholder': 'City'}))
    school_state    = forms.CharField(label="State", widget=forms.TextInput(attrs={'class':'required', 'placeholder': 'State'}), required=False)
    school_zip      = forms.CharField(label="Zip", widget=forms.TextInput(attrs={'class':'required zip', 'placeholder': 'Zip'}), min_length=5)
    school_country  = forms.CharField(label="Country", initial='United States of America', widget=forms.TextInput(attrs={'disabled': True, 'placeholder': 'Country'}), required=False)

    program_type        = forms.ChoiceField(label="What category best describes your program?", widget=forms.RadioSelect, choices=School.PROGRAM_TYPE_OPTIONS, initial=School.TYPE_CLUB)
    times_attended      = forms.IntegerField(label="Number of BMUN Sessions Attended", widget=forms.TextInput(attrs={'class':'required positive-integer', 'placeholder': 'Number of BMUN Sessions Attended'}))
    min_delegation_size = forms.IntegerField(label="Minimum Delegation Size", widget=forms.TextInput(attrs={'class':'required positive-integer', 'placeholder': 'Minimum Delegation Size'}))
    max_delegation_size = forms.IntegerField(label="Maximum Delegation Size", widget=forms.TextInput(attrs={'class':'required positive-integer', 'placeholder': 'Maximum Delegation Size'}))

    primary_name    = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'required', 'placeholder': 'Name'}))
    primary_email   = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'required email', 'placeholder': 'Email'}))
    primary_phone   = forms.CharField(label="Phone", widget=forms.TextInput(attrs={'class':'required phoneNum phoneVal', 'placeholder': 'Phone Number'}))
    secondary_name  = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'third', 'placeholder': 'Name'}), required=False)
    secondary_email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'email', 'placeholder': 'Email'}), required=False)
    secondary_phone = forms.CharField(label="Phone", widget=forms.TextInput(attrs={'class':'phoneNum phoneVal', 'placeholder': 'Phone Number'}), required=False)

    country_pref1  = forms.ChoiceField(label="01", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    country_pref2  = forms.ChoiceField(label="02", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    country_pref3  = forms.ChoiceField(label="03", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    country_pref4  = forms.ChoiceField(label="04", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    country_pref5  = forms.ChoiceField(label="05", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    country_pref6  = forms.ChoiceField(label="06", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    country_pref7  = forms.ChoiceField(label="07", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    country_pref8  = forms.ChoiceField(label="08", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    country_pref9  = forms.ChoiceField(label="09", widget=forms.Select(), choices=country_choices, required=False, initial=0)
    country_pref10 = forms.ChoiceField(label="10", widget=forms.Select(), choices=country_choices, required=False, initial=0)

    committee_prefs = forms.MultipleChoiceField(label="Special Committee Preferences", widget=forms.CheckboxSelectMultiple(),choices=special_committees_choices, required=False)

    
    # The following functions create the User and School entries in the
    # database. Run these only if the form is valid.
    
    def create_user(self, school):
        new_user = HuxleyUser.objects.create_user(self.cleaned_data['username'], self.cleaned_data['primary_email'], self.cleaned_data['password'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.school = school
        new_user.save()
        return new_user

    def create_school(self):
        registration_fee = 40.00 if date.today() < date(2013, 11, 01) else 50.00
        return School.objects.create(name=self.cleaned_data['school_name'],
                                     address=self.cleaned_data['school_address'],
                                     city=self.cleaned_data['school_city'],
                                     state=self.cleaned_data['school_state'],
                                     zip_code=self.cleaned_data['school_zip'],
                                     country=self.cleaned_data['school_country'],
                                     primary_name=self.cleaned_data['primary_name'],
                                     primary_email=self.cleaned_data['primary_email'],
                                     primary_phone=self.cleaned_data['primary_phone'],
                                     secondary_name=self.cleaned_data['secondary_name'],
                                     secondary_email=self.cleaned_data['secondary_email'],
                                     secondary_phone=self.cleaned_data['secondary_phone'],
                                     program_type=int(self.cleaned_data['program_type']),
                                     times_attended=self.cleaned_data['times_attended'],
                                     min_delegation_size=self.cleaned_data['min_delegation_size'],
                                     max_delegation_size=self.cleaned_data['max_delegation_size'],
                                     international=self.cleaned_data['school_location'] == School.LOCATION_INTERNATIONAL,
                                     registration_fee=registration_fee)

    def add_country_preferences(self, school):
        country_ids = [int(self.cleaned_data['country_pref%d' % i]) for i in xrange(1, 11)]
        school.update_country_preferences(country_ids)
        return True

    def add_committee_preferences(self, school):
        committee_ids = self.cleaned_data["committee_prefs"]
        school.update_committee_preferences(committee_ids)
        return True

    
    # Validation functions of the form clean_<field>. They return "cleaned"
    # versions of data supplied by the user.

    def clean_school_name(self):
        school_name = self.cleaned_data['school_name']
        if School.objects.filter(name=school_name).exists():
            raise forms.ValidationError('A school with the name "%s" has already been registered.' % (school_name))
        
        return school_name

    def clean_school_state(self):
        school_state = self.cleaned_data['school_state']
        if self.cleaned_data['school_location'] == School.LOCATION_USA and not school_state:
            raise forms.ValidationError('You must provide a state for a school in the United States.')

        return school_state

    def clean_school_country(self):
        school_country = self.cleaned_data['school_country']
        if self.cleaned_data['school_location'] == School.LOCATION_INTERNATIONAL and not school_country:
            raise forms.ValidationError('International schools must provide a country.')

        return school_country

    def clean_username(self):
        username = self.cleaned_data['username']
        if re.match("^[A-Za-z0-9\_\-]+$", username) is None:
            raise forms.ValidationError("Usernames must be alphanumeric, underscores, and/or hyphens only.")
        elif HuxleyUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username '%s' is already in use. Please choose another one." % (username))
        
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", password) is None:
            raise forms.ValidationError("Password contains invalid characters.")
        
        return password

    # Format: (123) 456-7890 || Note the space after the area code.
    def valid_phone_number(self, number, international):
        if international == School.LOCATION_INTERNATIONAL:
            return bool(re.match("^[0-9\-x\s\+\(\)]+$", number))
        else:
            return bool(re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", number))

    # General clean method
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        international = cleaned_data.get('school_location', School.LOCATION_USA)
        primary_phone = cleaned_data.get('primary_phone')
        secondary_phone = cleaned_data.get('secondary_phone')
        state = cleaned_data.get('school_state')
        country = cleaned_data.get('school_country')

        # Check to see if passwords match
        if password and password2 and password != password2:
            message = "Passwords do not match!"
            self._errors["password"] = self.error_class([message])
            self._errors["password2"] = self.error_class([message])
            # These fields are not valid anymore, so delete them from cleaned_data
            del cleaned_data["password"]
            del cleaned_data["password2"]

        # Check to see if the state is required
        if not state and international == "us":
            message = "This field is required."
            self._errors["school_state"] = self.error_class([message])
            del cleaned_data["school_state"]

        # Check to make sure phone number is formatted correctly
        if primary_phone and not self.valid_phone_number(primary_phone, international):
            message = "Phone in incorrect format."
            self._errors["primary_phone"] = self.error_class([message])
            del cleaned_data["primary_phone"]

        # Check to make sure phone number is formatted correctly
        if secondary_phone and not self.valid_phone_number(secondary_phone, international):
            message = "Phone in incorrect format."
            self._errors["secondary_phone"] = self.error_class([message])
            del cleaned_data["secondary_phone"]

        # Check to make sure a country is specified for international schools
        if international == "international":
            if not country or re.match("^\s*$", country) is not None:
                message = "You must specify a country."
                self._errors["school_country"] = self.error_class([message])
                
        # Always return cleaned_data
        return cleaned_data
