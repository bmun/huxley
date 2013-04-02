# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.core.urlresolvers import resolve
from django.http import HttpResponseForbidden

from huxley.core.models import AdvisorProfile, SecretariatProfile
from huxley.shortcuts import render_template

class EnforceUserTypeMiddleware:
    """ Enforces that users accessing URLs in the advisors or chairs app
        are advisors or chairs, respectively. Also sets request.profile to
        the user's AdvisorProfile or SecretariatProfile. """
    def process_request(self, request):
        app_name = resolve(request.path_info).app_name
        
        if app_name == 'advisors':
            profile_class, attr = AdvisorProfile, 'advisor_profile'
        elif app_name == 'chairs':
            profile_class, attr = SecretariatProfile, 'secretariat_profile'
        else:
            return

        if not request.user.is_authenticated():
            return render_template(request, 'auth.html')

        try:
            request.profile = getattr(request.user, attr)
        except profile_class.DoesNotExist:
            return HttpResponseForbidden()
