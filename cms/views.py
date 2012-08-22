from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.utils import simplejson

from forms.registration import RegistrationForm
from core.models import *

import datetime
import sys
import traceback
import re

# --------------------------
# --- PAGE DISPLAY VIEWS ---
# --------------------------

def register(request):
    c = RequestContext(request, {})
    state = ""
    username = password = ''
    c.update({'state':state})
    c.update({'username':username})
    c.update({'countries': Country.objects.filter(special=False).order_by('name')})
    c.update({'committees': Committee.objects.filter(special=True)})
    c.update({'selectionrange': range(1, 11)})

    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Creating a new user object
            newUser = User.objects.create_user(form.cleaned_data['Username'], \
                                               form.cleaned_data['PrimaryEmail'], \
                                               form.cleaned_data['Password'])
            newUser.first_name = form.cleaned_data['FirstName']
            newUser.last_name = form.cleaned_data['LastName']
            newUser.save()
                    
            # Creating a new school object
            newSchool = School.objects.create(name=form.cleaned_data['SchoolName'], \
                                              address=form.cleaned_data['SchoolAddress'], \
                                              city=form.cleaned_data['SchoolCity'], \
                                              state=form.cleaned_data['SchoolState'], \
                                              zip=form.cleaned_data['SchoolZip'], \
                                              primaryname = form.cleaned_data['PrimaryName'], \
                                              primaryemail = form.cleaned_data['PrimaryEmail'], \
                                              primaryphone = form.cleaned_data['PrimaryPhone'], \
                                              secondaryname = form.cleaned_data['SecondaryName'], \
                                              secondaryemail = form.cleaned_data['SecondaryEmail'], \
                                              secondaryphone = form.cleaned_data['SecondaryPhone'], \
                                              programtype = form.cleaned_data['programtype'], \
                                              timesattended = form.cleaned_data['howmany'], \
                                              mindelegationsize = form.cleaned_data['MinDelegation'], \
                                              maxdelegationsize = form.cleaned_data['MaxDelegation'], \
                                              international = form.cleaned_data['us_or_int'])
            newSchool.save()

            # TODO: get rid of the chunks below in favor of form object processing
            # Country Preferences
            countrypreferenceslist = []
            for num in range(1, 11):
                prefid = request.POST.get('CountryPref' + str(num))
                if prefid != "NULL":
                    countrypreferenceslist.append(Country.objects.get(id=prefid)) 

            # Add country preferences
            print "Country Preferences List: " + str(countrypreferenceslist)
            for country in countrypreferenceslist:
                print "Country " + str(country) + " is at index " + str(countrypreferenceslist.index(country))
                CountryPreference.objects.create(school=newSchool, country=country, rank=countrypreferenceslist.index(country) + 1).save()
                print "Adding " + str(country) + " to the school's preferences. Current list is " + str(newSchool.countrypreferences.all())
                        
            # Add committee preferences
            for committee in Committee.objects.filter(special=True):
                if committee.name in request.POST:
                    print "Adding " + committee.name + " to Committee Preferences of school " + newSchool.name
                    newSchool.committeepreferences.add(committee)
            newSchool.save()
                        
            newProfile = AdvisorProfile.objects.create(user=newUser, school=newSchool)
            newProfile.save()
                        
            return render_to_response('thanks.html', c)    
        else:
            print "FORM IS NOT VALID"        
                
    else:
        # Accessing for the first time
        form = RegistrationForm()

    return render_to_response('registration.html', {'form': form}, c)


# ------------------------
# --- HELPER FUNCTIONS ---
# ------------------------

def validate_pass_again(pass1, pass2):
        return pass1 == pass2

def validate_name(name):
        # Not much to check really, right?
        #I don't think checking that they're all roman alphabet characters is a good idea.
        return len(name) >= 1

def validate_pass(pass1):
        # How strong do you want their passwords to be?
        # Valid symbols: `~!@#$%^&*()-_+=?
        valid_pass = False
        if re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", pass1) is not None:
                valid_pass = True
        
        return (valid_pass and len(pass1) >= 6)

def validate_school_name(sname):
        unique = (len(School.objects.filter(name = sname)) == 0)        
        return (unique and validate_name(sname))

def validate_username(new_user):
    unique = (len(User.objects.filter(username=new_user)) == 0)
    # May only be alphanumeric characters, underscores
    valid_user = False
    if re.match("^[A-Za-z0-9\_]+$", new_user):
        valid_user = True
    return (unique and valid_user and len(new_user) >= 4)

def validate_unique_user(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        if User.objects.filter(username=username).exists():
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=406)

def validate_zip(zip):
        #properLen = (len(zip) == 5)
        #return (properLen and zip.isdigit())
        return zip.isdigit()

def validate_email(email):
        # Super LONG regex courtesy of http://www.ex-parrot.com/pdw/Mail-RFC822-Address.html
        # Figure out how to use super long regex later. Here's the naive version for now.
        #if re.match(".+@.+\..+", email):
        #        return True
        #else:
        #        return False
        if email_re.match(email):
            return True
        else:
            return False

def validate_phone(phoneNum):
        # Format: (123) 456-7890 || Note the space after the area code.
        if re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", phoneNum):
                return True
        else:
                return False
def validate_int_phone(phoneNum):
        if re.match("^[0-9\-x\s\+\(\)]+$", phoneNum):
                return True
        else:
                return False

def validate_number(numString):
        return numString.isdigit()

def validate_programtype(ptype):
        # Pretty simple
        return (ptype == "class" or ptype == "club")