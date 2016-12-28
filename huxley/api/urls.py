# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from huxley.api import views

urlpatterns = [
    url(r'^users/?$', views.user.UserList.as_view(), name='user_list'),
    url(r'^users/(?P<pk>[0-9]+)/?$', views.user.UserDetail.as_view(), name='user_detail'),
    url(r'^users/me/?$', views.user.CurrentUser.as_view(), name='current_user'),
    url(r'^users/me/password?$', views.user.UserPassword.as_view(), name='user_password'),

    url(r'^committees/?$', views.committee.CommitteeList.as_view(), name='committee_list'),
    url(r'^committees/(?P<pk>[0-9]+)/?$', views.committee.CommitteeDetail.as_view(), name='committee_detail'),

    url(r'^countries/?$', views.country.CountryList.as_view(), name='country_list'),
    url(r'^countries/(?P<pk>[0-9]+)/?$', views.country.CountryDetail.as_view(), name='country_detail'),

    url(r'^schools/?$', views.school.SchoolList.as_view(), name='school_list'),
    url(r'^schools/(?P<pk>[0-9]+)/?$', views.school.SchoolDetail.as_view(), name='school_detail'),
    url(r'^schools/(?P<pk>[0-9]+)/delegates/?$', views.school.SchoolDelegates.as_view(), name='school_delegates'),
    url(r'^schools/(?P<pk>[0-9]+)/invoice/?$', views.school.SchoolInvoice.as_view(), name='school_invoice'),

    url(r'^assignments/?$', views.assignment.AssignmentList.as_view(), name='assignment_list'),
    url(r'^assignments/(?P<pk>[0-9]+)/?$', views.assignment.AssignmentDetail.as_view(), name='assignment_detail'),

    url(r'^delegates/?$', views.delegate.DelegateList.as_view(), name='delegate_list'),
    url(r'^delegates/(?P<pk>[0-9]+)/?$', views.delegate.DelegateDetail.as_view(), name='delegate_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
