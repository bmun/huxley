# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET

from huxley.accounts.forms import RegistrationForm
from huxley.accounts.models import HuxleyUser
from huxley.core.models import *
from huxley.shortcuts import render_template, render_json


def login_user(request):
    '''Log in a user or render the login template.'''
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')

        user, error = HuxleyUser.authenticate(username, password)
        if error:
            return render_json({'success': False, 'error': error})

        redirect = HuxleyUser.login(request, user)
        return render_json({'success': True, 'redirect': redirect})

    return render_template(request, 'login.html')


def login_as_user(request, uid):
    '''Log in as a particular user (admin use only).'''
    try:
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        username = HuxleyUser.objects.get(id=uid).username
        user = authenticate(username=username, password=settings.ADMIN_SECRET)
        login(request, user)
        
        return HttpResponseRedirect(reverse('index'))

    except HuxleyUser.DoesNotExist:
        return HttpResponseNotFound()


def logout_user(request):
    '''Log out the current user. Although we'll only be supporting AJAX,
    we're leaving the standard logout here in case of a heinous bug that
    prevents normal logout.'''
    logout(request)
    if request.is_ajax():
        return HttpResponse(reverse('accounts:login'))
    else:
        return HttpResponseRedirect(reverse('index'))


def register(request):
    '''Register a new user and school.'''

    if not Conference.objects.get(session=62).open_reg:
        return render_template(request, 'registration-closed.html')

    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_school = form.create_school()
            new_user = form.create_user(new_school) 
            form.add_country_preferences(new_school)
            form.add_committee_preferences(new_school)
            
            if new_school.waitlist:
                return render_template(request, 'registration-waitlist.html')

            if not settings.DEBUG:
                new_user.email_user("Thanks for registering for BMUN 62!",
                                    "We're looking forward to seeing %s at BMUN 62. "
                                    "You can find information on deadlines and fees at "
                                    "http://bmun.org/bmun/timeline/. If you have any "
                                    "more questions, please feel free to email me at "
                                    "info@bmun.org. See you soon!\n\nBest,\n\nShrey Goel"
                                    "\nUSG of External Relations, BMUN 62" % new_school.name,
                                    "info@bmun.org")
            Conference.auto_country_assign(new_school) 
            return render_template(request, 'registration-success.html')

    form = RegistrationForm()
    context = {
        'form': form,
        'state': '',
        'countries': Country.objects.filter(special=False).order_by('name'),
        'committees': Committee.objects.filter(special=True),
        'waitlist': Conference.objects.get(session=62).waitlist_reg
    }

    return render_template(request, 'registration.html', context) 


@require_POST
def change_password(request):
    '''Attempt to change the user's password, or return an error.'''
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    old = request.POST.get('oldpassword')
    new = request.POST.get('newpassword')
    new2 = request.POST.get('newpassword2')

    success, error = request.user.change_password(old, new, new2)
    return HttpResponse('OK') if success else HttpResponse(error)


def reset_password(request):
    '''Reset a user's password.'''
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = HuxleyUser.reset_password(username)
        if new_password:
            if True:
                user.email_user("Huxley Password Reset",
                                "Your password has been reset to %s.\nThank you for using Huxley!" % (new_password),
                                from_email="no-reply@bmun.org")
            return render_template(request, 'password-reset-success.html')
        else:
            return render_template(request, 'password-reset.html', {'error': True})

    return render_template(request, 'password-reset.html')


@require_GET
def validate_unique_user(request):
    '''Check that a potential username is unique.'''
    username = request.GET['username']
    if HuxleyUser.objects.filter(username=username).exists():
        return HttpResponse(status=406)
    else:
        return HttpResponse(status=200)

