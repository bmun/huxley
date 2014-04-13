# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.core.urlresolvers import resolve
from django.http import HttpResponseForbidden

from huxley.shortcuts import render_template

class EnforceUserTypeMiddleware:
    """ Enforces that users accessing URLs in the advisors or chairs app
    are advisors or chairs, respectively."""
    def process_request(self, request):
        app_name = resolve(request.path_info).app_name

        if not app_name in ('advisors', 'chairs'):
            return

        if not request.user.is_authenticated():
            return render_template(request, 'login.html')

        if app_name == 'advisors' and not request.user.is_advisor():
            return HttpResponseForbidden()

        if app_name == 'chairs' and not request.user.is_chair():
            return HttpResponseForbidden()

