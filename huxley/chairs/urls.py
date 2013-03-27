# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf.urls import patterns, url

urlpatterns = patterns('huxley.chairs.views',
    url(r'^grading', 'grading', name='chair_grading'),
    url(r'^attendance', 'attendance', name='chair_attendance'),
    url(r'^help', 'help', name='chair_help'),
    url(r'^bugs', 'bugs', name='chair_bugs'),
)