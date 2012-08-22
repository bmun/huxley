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
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.create_user()                    
            new_school = form.create_school()
            form.add_country_preferences(new_school)
            form.add_committee_preferences(new_school)
            form.create_advisor_profile(new_user, new_school)
                        
            return render_to_response('thanks.html', context_instance=RequestContext(request))    
        else:
            print "> ERROR: FORM IS NOT VALID"        
    else:
        # Accessing for the first time
        form = RegistrationForm()

    countries = Country.objects.filter(special=False).order_by('name')
    committees = Committee.objects.filter(special=True)

    return render_to_response('registration.html', 
                                {'form': form, 'state':'', 
                                 'countries': countries,
                                 'committees': committees},
                                context_instance=RequestContext(request))


# ------------------------
# --- HELPER FUNCTIONS ---
# ------------------------

def validate_pass_again(pass1, pass2): # Done
        return pass1 == pass2

def validate_name(name): # Skip
        # Not much to check really, right?
        #I don't think checking that they're all roman alphabet characters is a good idea.
        return len(name) >= 1

def validate_pass(pass1): # Done
        # How strong do you want their passwords to be?
        # Valid symbols: `~!@#$%^&*()-_+=?
        valid_pass = False
        if re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", pass1) is not None:
                valid_pass = True
        
        return (valid_pass and len(pass1) >= 6)

def validate_school_name(sname): # Done
        unique = (len(School.objects.filter(name = sname)) == 0)        
        return (unique and validate_name(sname))

def validate_username(new_user): # Done
    unique = (len(User.objects.filter(username=new_user)) == 0)
    # May only be alphanumeric characters, underscores
    valid_user = False
    if re.match("^[A-Za-z0-9\_]+$", new_user):
        valid_user = True
    return (unique and valid_user and len(new_user) >= 4)

def validate_unique_user(request): # Keep here?
    if request.method == 'POST':
        username = request.POST.get('Username')
        if User.objects.filter(username=username).exists():
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=406)

def validate_zip(zip): # Done
        #properLen = (len(zip) == 5)
        #return (properLen and zip.isdigit())
        return zip.isdigit()

def validate_email(email): # Done
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

def validate_phone(phoneNum): # Done
        # Format: (123) 456-7890 || Note the space after the area code.
        if re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", phoneNum):
                return True
        else:
                return False
def validate_int_phone(phoneNum): # Done 
        if re.match("^[0-9\-x\s\+\(\)]+$", phoneNum):
                return True
        else:
                return False

def validate_number(numString): # Done, I think
        return numString.isdigit()

def validate_programtype(ptype): # Unnecessary
        # Pretty simple
        return (ptype == "class" or ptype == "club")