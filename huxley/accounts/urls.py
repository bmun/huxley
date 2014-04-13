# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf.urls import patterns, url

urlpatterns = patterns('huxley.accounts.views',
    url(r'^password/reset/?$', 'reset_password', name='reset_password'),
    url(r'^password/change/?$', 'change_password', name='change_password'),
    url(r'^register/?$', 'register', name='register'),
    url(r'^logout/?$', 'logout_user', name='logout'),
    url(r'^login/user/(?P<uid>\d+)/?$', 'login_as_user', name='login_as_user'),
    url(r'^login/?$', 'login_user', name='login'),
    url(r'^uniqueuser/?$', 'validate_unique_user', name='unique_user'),
)
