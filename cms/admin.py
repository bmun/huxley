#!/usr/bin/env python

from cms.models import *
from django.contrib import admin

admin.site.register(Conference)
admin.site.register(Country)
admin.site.register(School)
admin.site.register(Committee)
admin.site.register(Assignment)
admin.site.register(CountryPreference)
admin.site.register(HelpQuestion)
admin.site.register(HelpCategory)
admin.site.register(DelegateSlot)
admin.site.register(Delegate)
admin.site.register(UserProfile)