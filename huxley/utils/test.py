# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from huxley.accounts.models import HuxleyUser

class TestUsers():
    @staticmethod
    def new_user(**kwargs):
        u = HuxleyUser.objects.create_user(
            kwargs.get('username', 'testuser'),
            kwargs.get('email', 'test@user.in'),
            kwargs.get('password', 'test'))

        u.first_name = kwargs.get('first_name', 'Test')
        u.last_name = kwargs.get('last_name', 'User')

        for attr, value in kwargs.items():
            setattr(u, attr, value)

        u.save()
        return u

    @staticmethod
    def new_superuser(*args, **kwargs):
        kwargs['is_superuser'] = True
        return TestUsers.new_user(**kwargs)
