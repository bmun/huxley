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