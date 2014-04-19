# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.accounts.models import HuxleyUser

class TestUsers():
    @staticmethod
    def new_user(**kwargs):
        u = HuxleyUser(username=kwargs.get('username', 'testuser'),
                       email=kwargs.get('email', 'test@user.in'))
        u.set_password(kwargs.get('password', 'test'))

        u.first_name = kwargs.get('first_name', 'Test')
        u.last_name = kwargs.get('last_name', 'User')

        skip = {'username', 'email', 'password', 'first_name', 'last_name'}
        for attr, value in kwargs.items():
            if attr not in skip:
                setattr(u, attr, value)

        u.save()
        return u

    @staticmethod
    def new_superuser(*args, **kwargs):
        kwargs['is_superuser'] = True
        return TestUsers.new_user(**kwargs)
