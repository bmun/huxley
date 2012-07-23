from django import forms
from cms.models import *

class RegistrationForm(forms.Form):
    # TODO: don't know what to do about value
    # TODO: add other tags
    # By default, fields are required unless you specify required=False

    # User Information
    FirstName = forms.CharField(widget=forms.TextInput(attrs={'class':'half required'}))
    LastName = forms.CharField(widget=forms.TextInput(attrs={'class':'half required'}))
    Username = forms.CharField(widget=forms.TextInput(attrs={'class':'half required uniqueUser username'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'half required pass1 validChars'}))
    Password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'half required pass1 validChars'}))

    # School Information
    # TODO: Pick a default for international
    us_or_int = forms.ChoiceField(widget=forms.RadioSelect, choices=(('us', 'United States'), ('international', 'International')))
    SchoolName = forms.CharField(widget=forms.TextInput(attrs={'class':'full required'}))
    SchoolAddress = forms.CharField(widget=forms.TextInput(attrs={'class':'full required'}))
    SchoolCity = forms.CharField(widget=forms.TextInput(attrs={'class':'required'}))
    SchoolState = forms.CharField(widget=forms.TextInput(attrs={'class':'required'}))
    SchoolZip = forms.CharField(widget=forms.TextInput(attrs={'class':'required zip'}))
    SchoolCountry = forms.CharField(widget=forms.TextInput(attrs={'class':'showhide'}), required=False)

    # Program Information
    programtype = forms.ChoiceField(widget=forms.RadioSelect, choices=(('club', 'Club'), ('class', 'Class')))
    howmany = forms.IntegerField(widget=forms.TextInput(attrs={'class':'required IntegersOnly'}))
    MinDelegation = forms.IntegerField(widget=forms.TextInput(attrs={'class':'required IntegersOnly'}))
    MaxDelegation = forms.IntegerField(widget=forms.TextInput(attrs={'class':'required IntegersOnly'}))

    # Contact Information
    PrimaryName = forms.CharField(widget=forms.TextInput(attrs={'class':'required'}))
    PrimaryEmail = forms.EmailField(widget=forms.TextInput(attrs={'class':'required email'}))
    PrimaryPhone = forms.CharField(widget=forms.TextInput(attrs={'class':'required phoneNum phoneVal'}))
    SecondaryName = forms.CharField(widget=forms.TextInput(), required=False)
    SecondaryEmail = forms.EmailField(widget=forms.TextInput(attrs={'class':'email'}), required=False)
    SecondaryPhone = forms.CharField(widget=forms.TextInput(attrs={'class':'phoneNum phoneVal'}), required=False)

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
