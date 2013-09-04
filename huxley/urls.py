# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

admin.autodiscover()

urlpatterns = patterns('huxley.accounts.views',
    url(r'^password/reset', 'reset_password', name='reset_password'),
    url(r'^password/change', 'change_password', name='change_password'),
    url(r'^register', 'register', name='register'),
    url(r'^logout', 'logout_user', name='logout'),
    url(r'^login/user/(?P<uid>\d+)$', 'login_as_user', name='login_as_user'),
    url(r'^login', 'login_user', name='login'),
    url(r'^uniqueuser/', 'validate_unique_user', name='unique_user'),
)

urlpatterns += patterns('',
    url(r'^chair/', include('huxley.chairs.urls', app_name='chairs')),
    url(r'^advisor/', include('huxley.advisors.urls', app_name='advisors')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^about', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^success', TemplateView.as_view(template_name='thanks.html'), name='register_success'),
)

urlpatterns += patterns('',
    url(r'^$', 'huxley.core.views.index', name='index'),
)
