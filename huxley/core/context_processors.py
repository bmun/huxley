# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.core.urlresolvers import reverse
from django.http import HttpRequest

def conference(request):
    return {'conference' : request.conference}

def user_type(request):
    if not request.user.is_authenticated():
        return {}
    elif request.user.is_advisor():
        return {'user_type': 'advisor'}
    elif request.user.is_chair():
        return {'user_type': 'chair'}

def default_path(request):
    if not request.user.is_authenticated():
        return {'default_path': reverse('login')}
    return {'default_path': request.user.default_path()}