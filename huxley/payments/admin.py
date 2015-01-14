# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.contrib import admin
from huxley.payments.models import LineItem


admin.site.register(LineItem)
