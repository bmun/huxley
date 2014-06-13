# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.utils.shortcuts import render_template


def index(request):
    '''Render the appropriate base tempate.'''
    if not request.user.is_authenticated():
        return render_template(request, 'login.html')
    else:
        return render_template(request, 'base-inner.html')
