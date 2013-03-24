# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from functools import wraps
from django.http import HttpResponseForbidden
from huxley.core.models import AdvisorProfile
from huxley.shortcuts import render_template

def enforce_advisor():
	""" Enforces that the currently logged-in user is an advisor, and sets
		request.profile to be the user's AdvisorProfile. """
	def decorator(func):
		def inner_decorator(request, *args, **kwargs):
			if not request.user.is_authenticated():
				return render_template(request, 'auth.html')
			try:
				request.profile = request.user.advisor_profile
				return func(request, *args, **kwargs)
			except AdvisorProfile.DoesNotExist:
				return HttpResponseForbidden()
		
		return wraps(func)(inner_decorator)
	return decorator
