from django import forms
from cms.models import *
import re

class RegistrationForm(forms.Form):
    # TODO: don't know what to do about value
    # TODO: add other tags
    # By default, fields are required unless you specify required=False

    # User Information
    FirstName = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class':'half required'}))
    LastName = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class':'half required'}))
    Username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'half required uniqueUser username'}), min_length=4)
    Password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'half required pass1 validChars'}), min_length=6)
    Password2 = forms.CharField(label="Password (again)", widget=forms.PasswordInput(attrs={'class':'half required pass1 validChars'}))

    # School Information
    # TODO: Pick a default for international
    us_or_int = forms.ChoiceField(label="Where is your school?", widget=forms.RadioSelect(attrs={'class':'int_check', 'name':'us_or_int'}), choices=(('us', 'United States'), ('international', 'International')))
    SchoolName = forms.CharField(label="Official School Name", widget=forms.TextInput(attrs={'class':'full required'}))
    SchoolAddress = forms.CharField(label="Address", widget=forms.TextInput(attrs={'class':'full required'}))
    SchoolCity = forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'required'}))
    SchoolState = forms.CharField(label="State", widget=forms.TextInput(attrs={'class':'required'}))
    SchoolZip = forms.CharField(label="Zip", widget=forms.TextInput(attrs={'class':'required zip'}), min_length=5)
    SchoolCountry = forms.CharField(label="Country", widget=forms.TextInput(attrs={'class':'showhide'}), required=False)

    # Program Information
    programtype = forms.ChoiceField(label="What category best describes your program?", widget=forms.RadioSelect, choices=(('club', 'Club'), ('class', 'Class')))
    howmany = forms.IntegerField(label="Approximately how many times has your program attended BMUN?", widget=forms.TextInput(attrs={'class':'required IntegersOnly'}))
    MinDelegation = forms.IntegerField(label="Minimum", widget=forms.TextInput(attrs={'class':'required IntegersOnly'}))
    MaxDelegation = forms.IntegerField(label="Maximum", widget=forms.TextInput(attrs={'class':'required IntegersOnly'}))

    # Contact Information
    PrimaryName = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'required'}))
    PrimaryEmail = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'required email'}))
    PrimaryPhone = forms.CharField(label="Phone", widget=forms.TextInput(attrs={'class':'required phoneNum phoneVal'}))
    SecondaryName = forms.CharField(label="Name", widget=forms.TextInput(), required=False)
    SecondaryEmail = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'email'}), required=False)
    SecondaryPhone = forms.CharField(label="Phone", widget=forms.TextInput(attrs={'class':'phoneNum phoneVal'}), required=False)

    # Country Preferences (the ids)
    # TODO: Make sure this will work
    CountryPref1 = forms.CharField(widget=forms.TextInput)
    CountryPref2 = forms.CharField(widget=forms.TextInput)
    CountryPref3 = forms.CharField(widget=forms.TextInput)
    CountryPref4 = forms.CharField(widget=forms.TextInput)
    CountryPref5 = forms.CharField(widget=forms.TextInput)
    CountryPref6 = forms.CharField(widget=forms.TextInput)
    CountryPref7 = forms.CharField(widget=forms.TextInput)
    CountryPref8 = forms.CharField(widget=forms.TextInput)
    CountryPref9 = forms.CharField(widget=forms.TextInput)
    CountryPref10 = forms.CharField(widget=forms.TextInput)

    # Committee Preferences
    # TODO: Maybe leave this to views.py

    # Validation
    # Format: clean_<field>
    def clean_SchoolName(self):
        # Check for uniqueness
        school_name = self.cleaned_data['SchoolName']
        unique = len(School.objects.filter(name = school_name)) == 0
        if not unique:
            raise forms.ValidationError("A school with this name has already been registered.")
        # Return data, whether changed or not
        return school_name


    def clean_Username(self):
        # Check for uniqueness
        username = self.cleaned_data['Username']
        unique = len(User.objects.filter(username=username)) == 0
        if not unique:
            raise forms.ValidationError("This username is already in use. Please choose another one.")
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


    def clean_PrimaryPhone(self):
        phone_num = self.cleaned_data['PrimaryPhone']
        international = self.cleaned_data['us_or_int']

        if not phone_num_is_valid(phone_num, international):
            raise forms.ValidationError("Phone number in incorrect format. Format: (XXX) XXX-XXXX")
        # Return data, changed or not
        return primary_phone


    def clean_SecondaryPhone(self):
        phone_num = self.cleaned_data['SecondaryPhone']
        international = self.cleaned_data['us_or_int']

        if not phone_num_is_valid(phone_num, international):
            raise forms.ValidationError("Phone number in incorrect format. Format: (XXX) XXX-XXXX")
        # Return data, changed or not
        return primary_phone


    def phone_num_is_valid(number, international):
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

        if Password and Password2:
            if Password != Password2:
                raise forms.ValidationError("Passwords must match!")

        # Always return cleaned_data
        return cleaned_data

