# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from itertools import izip_longest

def render_template(request, template, context=None):
    '''Wrap render_to_response with the context_instance argument set.'''
    return render_to_response(template, context,
                              context_instance=RequestContext(request))

def render_json(data):
    '''Return an HttpResponse object containing json-encoded data.'''
    return HttpResponse(simplejson.dumps(data), content_type='application/json')

def pairwise(iterable):
    '''Group the elements of the given interable into 2-tuples.'''
    i = iter(iterable)
    return izip_longest(i, i)
