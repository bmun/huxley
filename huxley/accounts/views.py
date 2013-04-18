# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotAllowed, HttpResponseNotFound, \
                        HttpResponseForbidden
from django.utils import simplejson
from django.views.decorators.http import require_POST, require_GET

from huxley.accounts.forms.registration import RegistrationForm
from huxley.accounts.forms.forgot_password import ForgotPasswordForm
from huxley.core.models import *
from huxley.shortcuts import render_template

import re

# Logs in a user or renders the login template.
def login_user(request):
    """ Logs in a user or renders the login template. """
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
            return render_template(request, 'auth.html', {'state': error})
        else:
            return HttpResponseRedirect(reverse('index'))

    return render_template(request, 'auth.html')


def login_as_user(request, uid):
    """ Logs in as a particular user (admin use only). """
    try:
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        username = User.objects.get(id=uid).username
        user = authenticate(username=username, password=settings.ADMIN_SECRET)
        login(request, user)
        
        return HttpResponseRedirect(reverse('index'))

    except User.DoesNotExist:
        return HttpResponseNotFound()


def logout_user(request):
    """ Logs out the current user. """
    logout(request)
    if request.is_ajax():
        return HttpResponse(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('index'))


def register(request):
    """ Registers a new user and school. """

    # Registration is closed.
    return render_template(request, 'registration_closed.html')

    if request.method =='POST':
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
            return render_template(request, 'thanks.html')    
    else:
        # Accessing for the first time
        form = RegistrationForm()

    context = {
        'form': form,
        'state': '',
        'countries': Country.objects.filter(special=False).order_by('name'),
        'committees': Committee.objects.filter(special=True)
    }

    return render_template(request, 'registration.html', context) 


@require_POST
def change_password(request):
    """ Attempts to change the user's password, or returns an error. """
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


def forgot_password(request):
    """ Resets a user's password. """
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            new_pass = form.reset_pass(user)
            user.email_user("Huxley Password Reset",
                            "Your password has been reset to %s.\nThank you for using Huxley!" % (new_pass),
                            from_email="no-reply@bmun.org")

            return render_template(request, 'reset_success.html')

    else:
        form = ForgotPasswordForm()

    return render_template(request, 'forgot_password.html', {'form': form})


@require_GET
def validate_unique_user(request):
    """ Checks that a potential username is unique. """
    username = request.GET['username']
    if User.objects.filter(username=username).exists():
        return HttpResponse(status=406)
    else:
        return HttpResponse(status=200)

