# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf.urls import patterns, url

urlpatterns = patterns('huxley.www.views',
    # Match any URL and let the client take care of routing.
    url(r'', 'index', name='index'),
)
