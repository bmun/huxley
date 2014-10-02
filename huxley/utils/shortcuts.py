# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.shortcuts import render_to_response
from django.template import RequestContext


def render_template(request, template, context=None):
    '''Wrap render_to_response with the context_instance argument set.'''
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
