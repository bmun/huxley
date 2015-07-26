# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.contrib import admin
from huxley.logging.models import LogEntry

admin.site.register(LogEntry)
