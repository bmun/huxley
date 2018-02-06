#!/usr/bin/env python

# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.contrib import admin

from huxley.core.models import *

from .assignment import AssignmentAdmin
from .committee import CommitteeAdmin
from .country import CountryAdmin
from .delegate import DelegateAdmin
from .schools import SchoolAdmin
from .registration import RegistrationAdmin
from .position_paper import PositionPaperAdmin

admin.site.register(Conference)
admin.site.register(Country, CountryAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(CommitteeFeedback)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(CountryPreference)
admin.site.register(Delegate, DelegateAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Rubric)
admin.site.register(PositionPaper, PositionPaperAdmin)
