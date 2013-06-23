#!/usr/bin/env python

# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib import admin
from huxley.accounts.models import HuxleyUser

admin.site.register(HuxleyUser)