# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET

from huxley.accounts.forms import ForgotPasswordForm, RegistrationForm
from huxley.accounts.models import HuxleyUser
from huxley.core.models import *
from huxley.shortcuts import render_template, render_json

import re

def login_user(request):
    """ Logs in a user or renders the login template. """
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')

        user, error = HuxleyUser.authenticate(username, password)
        if error:
            return render_json({'success': False, 'error': error})

        redirect = HuxleyUser.login(request, user)
        return render_json({'success': True, 'redirect': redirect})

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
    """ Logs out the current user. Although we'll only be supporting AJAX,
        we're leaving the standard logout here in case of a heinous bug that
        prevents normal logout."""
    logout(request)
    if request.is_ajax():
        return HttpResponse(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('index'))


def register(request):
    """ Registers a new user and school. """

    # Registration is closed. TODO: Implement the waitlist.
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
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    old = request.POST.get('oldpassword')
    new = request.POST.get('newpassword')
    new2 = request.POST.get('newpassword2')

    success, error = HuxleyUser.change_password(request.user, old, new, new2)
    return HttpResponse('OK') if success else HttpResponse(error)


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

