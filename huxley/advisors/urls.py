# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf.urls import patterns, url

urlpatterns = patterns('huxley.advisors.views',
    url(r'^welcome', 'welcome', name='welcome'),
    url(r'^preferences', 'preferences', name='preferences'),
    url(r'^roster', 'roster', name='roster'),
    url(r'^attendance', 'attendance', name='attendance'),
    url(r'^help', 'help', name='help'),
)
