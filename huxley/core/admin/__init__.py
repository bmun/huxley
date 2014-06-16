#!/usr/bin/env python

# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.contrib import admin

from huxley.core.models import *

from .assignment import AssignmentAdmin
from .committee import CommitteeAdmin
from .country import CountryAdmin
from .delegate import DelegateAdmin


admin.site.register(Conference)
admin.site.register(Country, CountryAdmin)
admin.site.register(School)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(CountryPreference)
admin.site.register(HelpQuestion)
admin.site.register(HelpCategory)
admin.site.register(DelegateSlot)
admin.site.register(Delegate, DelegateAdmin)
