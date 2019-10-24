# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import (HttpResponseRedirect, HttpResponseNotFound,
                         HttpResponseForbidden)

from huxley.accounts.models import User
from huxley.core.models import *


def login_as_user(request, uid):
    '''Log in as a particular user (admin use only).'''
    try:
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        username = User.objects.get(id=uid).username
        user = authenticate(username=username, password=settings.ADMIN_SECRET)
        login(request, user)

        return HttpResponseRedirect(reverse('www:index'))

    except User.DoesNotExist:
        return HttpResponseNotFound()


def logout_user(request):
    '''Log out the current user. Although we'll only be supporting AJAX,
    we're leaving the standard logout here in case of a heinous bug that
    prevents normal logout.'''
    logout(request)
    return HttpResponseRedirect(reverse('www:index'))
