# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from huxley.api import views

urlpatterns = patterns('',
    url(r'^users/?$', views.UserList.as_view(), name='user_list'),
    url(r'^users/(?P<pk>[0-9]+)/?$', views.UserDetail.as_view(), name='user_detail'),
)

urlpatterns += patterns('',
    url(r'^committees/?$', views.CommitteeList.as_view(), name='committee_list'),
    url(r'^committees/(?P<pk>[0-9]+)/?$', views.CommitteeDetail.as_view(), name='committee_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
