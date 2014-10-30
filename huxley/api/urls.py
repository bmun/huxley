# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from huxley.api import views

urlpatterns = patterns('',
    url(r'^users/?$', views.user.UserList.as_view(), name='user_list'),
    url(r'^users/(?P<pk>[0-9]+)/?$', views.user.UserDetail.as_view(), name='user_detail'),
    url(r'^users/me/?$', views.user.CurrentUser.as_view(), name='current_user'),
    url(r'^users/me/password?$', views.user.UserPassword.as_view(), name='user_password'),
)

urlpatterns += patterns('',
    url(r'^committees/?$', views.committee.CommitteeList.as_view(), name='committee_list'),
    url(r'^committees/(?P<pk>[0-9]+)/?$', views.committee.CommitteeDetail.as_view(), name='committee_detail'),
)

urlpatterns += patterns('',
    url(r'^countries/?$', views.country.CountryList.as_view(), name='country_list'),
    url(r'^countries/(?P<pk>[0-9]+)/?$', views.country.CountryDetail.as_view(), name='country_detail'),
)

urlpatterns += patterns('',
    url(r'^schools/?$', views.school.SchoolList.as_view(), name='school_list'),
    url(r'^schools/(?P<pk>[0-9]+)/?$', views.school.SchoolDetail.as_view(), name='school_detail'),
    url(r'^schools/(?P<pk>[0-9]+)/assignments/?$', views.school.SchoolAssignments.as_view(), name='school_assignments'),
    url(r'^schools/(?P<pk>[0-9]+)/invoice/?$', views.school.SchoolInvoice.as_view(), name='school_invoice')
)

urlpatterns = format_suffix_patterns(urlpatterns)
