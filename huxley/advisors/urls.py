# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf.urls import patterns, url

urlpatterns = patterns('huxley.advisors.views',
<<<<<<< HEAD
    url(r'^welcome/?$', 'welcome', name='welcome'),
    url(r'^preferences/?$', 'preferences', name='preferences'),
    url(r'^roster/?$', 'roster', name='roster'),
    url(r'^attendance/?$', 'attendance', name='attendance'),
    url(r'^help/?$', 'help', name='help'),
=======
    url(r'^welcome', 'welcome', name='welcome'),
    url(r'^preferences', 'preferences', name='preferences'),
    url(r'^roster', 'roster', name='roster'),
    url(r'^attendance', 'attendance', name='attendance'),
    url(r'^help', 'help', name='help'),
    url(r'^summaries_advisors', 'summaries_advisors', name='summaries_advisors'),
>>>>>>> Attendance is working. Added a dedelegate summaries tab so that chairs can give a summary of each delegate's performance over the weekend and advisors can view. May need to readjust layout for attendance.
)
