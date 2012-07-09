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
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'showhide'}))

    # Program Information
    programtype = forms.ChoiceField(widget=forms.RadioSelect, choices=(('club', 'Club'), ('class', 'Class')))
    howmany = forms.CharField(widget=forms.IntegerInput(attrs={'class':'required IntegersOnly'}))
    min_delegation = forms.CharField(widget=forms.IntegerInput(attrs={'class':'required IntegersOnly'}))
    max_delegation = forms.CharField(widget=forms.IntegerInput(attrs={'class':'required IntegersOnly'}))

    # Contact Information
    primary_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required'}))
    primary_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'required email'}))
    primary_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'required phoneNum phoneVal'}))
    secondary_name = forms.CharField(widget=forms.TextInput())
    secondary_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'email'}))
    secondary_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'phoneNum phoneVal'}))

    # Preferences
    # TODO: Add this