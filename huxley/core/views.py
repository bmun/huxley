# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.http import require_POST

from huxley.core.models import *
from huxley.core.forms.registration import RegistrationForm
from huxley.core.forms.forgot_password import ForgotPasswordForm

import re

# Renders the appropriate base index template.
def index(request):
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return render_to_response('auth.html', context)
    elif SecretariatProfile.objects.filter(user=request.user).exists():
        return render_to_response('secretariat_index.html', context)
    else:
        return render_to_response('advisor_index.html', context)


# Logs in a user or renders the login template.
def login_user(request):
    if request.method == "POST":    
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        error = ""
        
        # Determine if the login is valid.
        if not (username and password):
            error = "Woops! One or more of the fields is blank."
        elif user is None:
            error = "Sorry! The login you provided was invalid."
        elif not user.is_active:
            error = "We're sorry, but your account is inactive."
        else:
            login(request, user)
        
        # Determine the appropriate response.
        if request.is_ajax():
            if error:
                response = {"success": False, "error": error}
            elif SecretariatProfile.objects.filter(user=user).exists():
                response = {"success": True,
                            "redirect": reverse('chair_attendance')}
            else:
                response = {"success": True,
                            "redirect": reverse('advisor_welcome')}
            
            return HttpResponse(simplejson.dumps(response),
                                mimetype='application/json')
        elif error:
            c = RequestContext(request, {'state':error})
            return render_to_response('auth.html', c)
        else:
            return HttpResponseRedirect(reverse('index'))
        
    c = RequestContext(request)
    return render_to_response('auth.html', c)


# Logs in as a particular user (admin use only).
def login_as_user(request, uid):
    try:
        if not request.user.is_superuser:
            return HttpResponse(status=403)

        username = User.objects.get(id=uid).username
        user = authenticate(username=username, password=settings.ADMIN_SECRET)
        login(request, user)
        
        return HttpResponseRedirect(reverse('index'))

    except ObjectDoesNotExist:
        return HttpResponse(status=404)


# Logs out the current user.
def logout_user(request):
    logout(request)
    if request.is_ajax():
        return HttpResponse(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('index'))


# Registers a new user and school
def register(request):

    # Registration is closed.
    return render_to_response('registration_closed.html', context_instance=RequestContext(request))

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.create_user()                    
            new_school = form.create_school()
            form.add_country_preferences(new_school)
            form.add_committee_preferences(new_school)
            form.create_advisor_profile(new_user, new_school)
            
            new_user.email_user("Thanks for registering for BMUN 61!",
                                "We're looking forward to seeing %s at BMUN 61. "
                                "You can find information on deadlines and fees at "
                                "http://bmun.org/bmun/timeline/. If you have any "
                                "more questions, please feel free to email me at "
                                "info@bmun.org. See you soon!\n\nBest,\n\nNishita Agarwal"
                                "\nUSG of External Relations, BMUN 61" % new_school.name,
                                "info@bmun.org")            
            return render_to_response('thanks.html', context_instance=RequestContext(request))    
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


#Attempts to change the current user's password, or returns an error.
@require_POST
def change_password(request):
    oldpass = request.POST.get('oldpassword')
    newpass = request.POST.get('newpassword')
    newpass2 = request.POST.get('newpassword2')
    
    if not request.user.is_authenticated():
        return HttpResponse(status=401)
    elif not (oldpass or newpass or newpass2):
        return HttpResponse("One or more fields is blank.")
    elif newpass != newpass2:
        return HttpResponse("New passwords must match.")
    elif len(newpass) < 6:
        return HttpResponse("New password must be at least 6 characters long.")
    elif not re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", newpass):
        return HttpResponse("New password must have only alphanumeric "
                            "characters and symbols (above letters)")
    elif not request.user.check_password(oldpass):
        return HttpResponse("Incorrect password.")
    else:
        request.user.set_password(newpass)
        request.user.save();
        return HttpResponse('OK')


# Resets a user's password.
def forgot_password(request):
    context = RequestContext(request)
    if request.POST:
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            new_pass = form.reset_pass(user)
            user.email_user("Huxley Password Reset",
                            "Your password has been reset to %s.\nThank you for using Huxley!" % (new_pass),
                            from_email="no-reply@bmun.org")

            return render_to_response('reset_success.html',
                                      context_instance=context)
    else:
        form = ForgotPasswordForm()

    return render_to_response('forgot_password.html', {"form":form},
                              context_instance=context)


# Checks that a username is unique.
def validate_unique_user(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        if User.objects.filter(username=username).exists():
            return HttpResponse(status=406)
        else:
            return HttpResponse(status=200)
