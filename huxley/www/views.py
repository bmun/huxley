# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.shortcuts import render_to_response

def index(request):
    return render_to_response('www.html')
