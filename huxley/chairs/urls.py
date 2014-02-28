# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf.urls import patterns, url

urlpatterns = patterns('huxley.chairs.views',
<<<<<<< HEAD
    url(r'^grading/?$', 'grading', name='grading'),
    url(r'^attendance/?$', 'attendance', name='attendance'),
    url(r'^help/?$', 'help', name='help'),
    url(r'^bugs/?$', 'bugs', name='bugs'),
=======
    url(r'^summaries', 'summaries', name='summaries'),
    url(r'^attendance', 'attendance', name='attendance'),
    url(r'^help', 'help', name='help'),
    url(r'^bugs', 'bugs', name='bugs'),
>>>>>>> Attendance is working. Added a dedelegate summaries tab so that chairs can give a summary of each delegate's performance over the weekend and advisors can view. May need to readjust layout for attendance.
)
