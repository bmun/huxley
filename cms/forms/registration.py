from django import forms

class RegistrationForm(forms.Form):
    # TODO: don't know what to do about value
    # TODO: add other tags
    # By default, fields are required unless you specify required=False

    # User Information
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'half required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'half required'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'half required uniqueUser username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'half required pass1 validChars'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'half required pass1 validChars'}))

    # School Information
    # TODO: Pick a default for international
    international = forms.ChoiceField(widget=forms.RadioSelect, choices=(('us', 'United States'), ('int', 'International')))
    school_name = forms.CharField(widget=forms.TextInput(attrs={'class':'full required'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'full required'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'required'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'required'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class':'required zip'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'showhide'}), required=False)

    # Program Information
    programtype = forms.ChoiceField(widget=forms.RadioSelect, choices=(('club', 'Club'), ('class', 'Class')))
    howmany = forms.CharField(widget=forms.IntegerInput(attrs={'class':'required IntegersOnly'}))
    min_delegation = forms.CharField(widget=forms.IntegerInput(attrs={'class':'required IntegersOnly'}))
    max_delegation = forms.CharField(widget=forms.IntegerInput(attrs={'class':'required IntegersOnly'}))

    # Contact Information
    primary_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required'}))
    primary_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'required email'}))
    primary_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'required phoneNum phoneVal'}))
    secondary_name = forms.CharField(widget=forms.TextInput(), required=False)
    secondary_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'email'}), required=False)
    secondary_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'phoneNum phoneVal'}), required=False)

    # Country Preferences
    # TODO: Make sure this will work
    countrypref1 = forms.CharField(widget=forms.TextInput)
    countrypref2 = forms.CharField(widget=forms.TextInput)
    countrypref3 = forms.CharField(widget=forms.TextInput)
    countrypref4 = forms.CharField(widget=forms.TextInput)
    countrypref5 = forms.CharField(widget=forms.TextInput)
    countrypref6 = forms.CharField(widget=forms.TextInput)
    countrypref7 = forms.CharField(widget=forms.TextInput)
    countrypref8 = forms.CharField(widget=forms.TextInput)
    countrypref9 = forms.CharField(widget=forms.TextInput)
    countrypref10 = forms.CharField(widget=forms.TextInput)

    # Committee Preferences
    # TODO: Maybe leave this to views.py