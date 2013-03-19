# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from core.models import Conference
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

class LatestConferenceMiddleware:
    def process_request(self, request):
        try:
            request.conference = Conference.objects.latest()
        except ObjectDoesNotExist:
            request.conference = None