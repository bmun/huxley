#!/usr/bin/env python

# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

from huxley.accounts.models import User


class UserAdmin(UserAdminBase):
    model = User
    fieldsets = UserAdminBase.fieldsets + (
        ('BMUN-Specific Information', {
            'fields': (
                'user_type',
                'school',
                'committee',
                'delegate',
            )
        }),
    )


admin.site.register(User, UserAdmin)
