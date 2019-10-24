# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('huxley.api.urls', namespace='api')),
    path('', include('huxley.www.urls', namespace='www')),
    re_path('favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
]
