# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.conf import settings

class LoginAsUserBackend:
    def authenticate(self, username=None, password=None):
        if settings.ADMIN_SECRET and password == settings.ADMIN_SECRET:
            try:
                return HuxleyUser.objects.get(username=username)
            except:
                pass
        return None

    def get_user(self, user_id):
        try:
            return HuxleyUser.objects.get(pk=user_id)
        except:
            return None
