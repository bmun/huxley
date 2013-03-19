# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.http import HttpRequest

def conference(request):
    return {'conference' : request.conference}