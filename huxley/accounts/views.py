# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET

from huxley.accounts.models import User
from huxley.accounts.exceptions import AuthenticationError
from huxley.core.models import *
from huxley.utils.shortcuts import render_template, render_json


def login_user(request):
    '''Log in a user or render the login template.'''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.authenticate(username, password)
        except AuthenticationError as e:
            return render_json({'success': False, 'error': str(e)})

        redirect = User.login(request, user)
        return render_json({'success': True, 'redirect': redirect})

    return render_template(request, 'login.html')


def login_as_user(request, uid):
    '''Log in as a particular user (admin use only).'''
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
    raise Http404


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
        new_password = User.reset_password(username)
        if new_password:
            return render_template(request, 'password-reset-success.html')
        else:
            return render_template(request, 'password-reset.html', {'error': True})

    return render_template(request, 'password-reset.html')


@require_GET
def validate_unique_user(request):
    '''Check that a potential username is unique.'''
    username = request.GET['username']
    if User.objects.filter(username=username).exists():
        return HttpResponse(status=406)
    else:
        return HttpResponse(status=200)

