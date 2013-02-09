#!/usr/bin/env python

# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from core.models import *
from django.contrib import admin

class DelegateAdmin(admin.ModelAdmin):
    def roster(self, request):
        return HttpResponseRedirect(
                reverse("admin:core_delegate_changelist")
        )

    def get_urls(self):
        from django.conf.urls.defaults import *
        urls = super(DelegateAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'roster',
                self.admin_site.admin_view(self.roster),
                name='core_delegate_roster',
            ),
        )
        return my_urls + urls

admin.site.register(Conference)
admin.site.register(Country)
admin.site.register(School)
admin.site.register(Committee)
admin.site.register(Assignment)
admin.site.register(CountryPreference)
admin.site.register(HelpQuestion)
admin.site.register(HelpCategory)
admin.site.register(DelegateSlot)
admin.site.register(Delegate, DelegateAdmin)