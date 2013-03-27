# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponseForbidden

from huxley.core.models import *

class LatestConferenceMiddleware:
    """ Sets request.conference to the latest instance of Conference. """
    def process_request(self, request):
        try:
            request.conference = Conference.objects.latest()
        except ObjectDoesNotExist:
            request.conference = None

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

        try:
            request.profile = getattr(request.user, attr)
        except profile_class.DoesNotExist:
            return HttpResponseForbidden()
