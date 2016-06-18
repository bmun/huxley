# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf.urls import url

from huxley.www import views


urlpatterns = [
    # Match any URL and let the client take care of routing.
    url(r'', views.index, name='index'),
]
