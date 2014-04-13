# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.core.models import Conference

class LatestConferenceMiddleware:
    """ Sets request.conference to the latest instance of Conference. """
    def process_request(self, request):
        try:
            request.conference = Conference.objects.latest()
        except Conference.DoesNotExist:
            request.conference = None
