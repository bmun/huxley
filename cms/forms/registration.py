from django import forms

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
    us_or_int = forms.ChoiceField(widget=forms.RadioSelect, choices=(('us', 'United States'), ('int', 'International')))
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

    # Country Preferences
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