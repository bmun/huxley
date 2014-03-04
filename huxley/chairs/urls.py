# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf.urls import patterns, url

urlpatterns = patterns('huxley.chairs.views',
    url(r'^summaries', 'summaries', name='summaries'),
    url(r'^attendance', 'attendance', name='attendance'),
    url(r'^help', 'help', name='help'),
    url(r'^bugs', 'bugs', name='bugs'),
)
