# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf import settings

from huxley.accounts.models import User


class LoginAsUserBackend:
    def authenticate(self, username=None, password=None):
        if settings.ADMIN_SECRET and password == settings.ADMIN_SECRET:
            try:
                return User.objects.get(username=username)
            except:
                pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
