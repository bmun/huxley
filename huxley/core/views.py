# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.shortcuts import render_to_response
from django.template import RequestContext

from huxley.core.models import *


# Renders the appropriate base index template.
def index(request):
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return render_to_response('auth.html', context)
    elif SecretariatProfile.objects.filter(user=request.user).exists():
        return render_to_response('secretariat_index.html', context)
    else:
        return render_to_response('advisor_index.html', context)
