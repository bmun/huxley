# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'huxley.core.views.index', name='index'),
    url(r'^', include('huxley.accounts.urls', app_name='accounts', namespace='accounts')),
    url(r'^www/', include('huxley.www.urls', app_name='www', namespace='www')),
    url(r'^api/', include('huxley.api.urls', app_name='api', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
)
