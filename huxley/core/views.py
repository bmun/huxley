# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.shortcuts import render_to_response
from django.template import RequestContext

from huxley.core.models import *

def index(request):
    '''Render the appropriate base tempate.'''
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return render_to_response('auth.html', context)
    else:
        return render_to_response('base_index.html', context)
