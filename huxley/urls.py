# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('huxley.accounts.urls', app_name='accounts', namespace='accounts')),
    url(r'^chair/', include('huxley.chairs.urls', app_name='chairs', namespace='chairs')),
    url(r'^advisor/', include('huxley.advisors.urls', app_name='advisors', namespace='advisors')),
    url(r'^api/', include('huxley.api.urls', app_name='api', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^about/?$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^success/?$', TemplateView.as_view(template_name='registration-success.html'), name='register_success'),
)

urlpatterns += patterns('',
    url(r'^$', 'huxley.core.views.index', name='index'),
)
