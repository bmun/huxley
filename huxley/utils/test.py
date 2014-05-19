# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.accounts.models import HuxleyUser
from huxley.core.models import School, Committee

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

class TestSchools():
    @staticmethod
    def new_school(**kwargs):
        s = School(name=kwargs.get('name', 'Test School'),
                   address=kwargs.get('address', '1 Schoolhouse Road'),
                   city=kwargs.get('city', 'Berkeley'),
                   state=kwargs.get('state', 'CA'),
                   zip_code=kwargs.get('zip_code', '94024'),
                   country=kwargs.get('country', 'United States of America'),
                   primary_name=kwargs.get('primary_name', ''),
                   primary_email=kwargs.get('primary_email', ''),
                   primary_phone=kwargs.get('primary_phone', ''),
                   secondary_name=kwargs.get('secondary_name', ''),
                   secondary_email=kwargs.get('secondary_email', ''),
                   secondary_phone=kwargs.get('secondary_phone', ''),
                   program_type=kwargs.get('program_type', School.TYPE_CLUB),
                   times_attended=kwargs.get('times_attended', 0),
                   min_delegation_size=kwargs.get('min_delegation_size', 0),
                   max_delegation_size=kwargs.get('max_delegation_size', 0))

        skip = {'name', 'address', 'city', 'state', 'zip_code', 'country',
                'primary_name', 'primary_email', 'primary_phone',
                'secondary_name', 'secondary_email', 'secondary_phone',
                'program_type', 'times_attended', 'min_delegation_size',
                'max_delegation_size'}
        for attr, value in kwargs.items():
            if attr not in skip:
                setattr(s, attr, value)

        s.save()
        TestUsers.new_user(school=s, committee=TestCommittees.new_committee())
        return s

class TestCommittees():
    @staticmethod
    def new_committee(**kwargs):
        c = Committee(
                name=kwargs.get('name', 'testCommittee'),
                full_name=kwargs.get('fullName', 'testCommittee'),
                delegation_size=kwargs.get('delegation_size', 10),
                special=kwargs.get('special', False))
        c.save()
        return c
