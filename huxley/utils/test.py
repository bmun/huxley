# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import csv
import StringIO

from huxley.accounts.models import User
from huxley.core.models import School, Committee, Country


class TestUsers():
    @staticmethod
    def new_user(**kwargs):
        u = User(username=kwargs.pop('username', 'testuser'),
                 email=kwargs.pop('email', 'test@user.in'))
        u.set_password(kwargs.pop('password', 'test'))

        u.first_name = kwargs.pop('first_name', 'Test')
        u.last_name = kwargs.pop('last_name', 'User')

        for attr, value in kwargs.items():
            setattr(u, attr, value)

        u.save()
        return u

    @staticmethod
    def new_superuser(*args, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return TestUsers.new_user(**kwargs)


class TestSchools():
    @staticmethod
    def new_school(**kwargs):
        s = School(name=kwargs.pop('name', 'Test School'),
                   address=kwargs.pop('address', '1 Schoolhouse Road'),
                   city=kwargs.pop('city', 'Berkeley'),
                   state=kwargs.pop('state', 'CA'),
                   zip_code=kwargs.pop('zip_code', '94024'),
                   country=kwargs.pop('country', 'United States of America'),
                   primary_name=kwargs.pop('primary_name', ''),
                   primary_gender=kwargs.pop('primary_gender', School.GENDER_MALE),
                   primary_email=kwargs.pop('primary_email', ''),
                   primary_phone=kwargs.pop('primary_phone', ''),
                   primary_type=kwargs.pop('primary_type', School.TYPE_FACULTY),
                   secondary_name=kwargs.pop('secondary_name', ''),
                   secondary_gender=kwargs.pop('secondary_gender', School.GENDER_MALE),
                   secondary_email=kwargs.pop('secondary_email', ''),
                   secondary_phone=kwargs.pop('secondary_phone', ''),
                   secondary_type=kwargs.pop('secondary_type', School.TYPE_FACULTY),
                   program_type=kwargs.pop('program_type', School.TYPE_CLUB),
                   times_attended=kwargs.pop('times_attended', 0),
                   delegation_size=kwargs.pop('delegation_size', 0))

        for attr, value in kwargs.items():
            setattr(s, attr, value)

        s.save()
        TestUsers.new_user(school=s, committee=TestCommittees.new_committee())
        return s


class TestCommittees():
    @staticmethod
    def new_committee(**kwargs):
        c = Committee(
                name=kwargs.pop('name', 'testCommittee'),
                full_name=kwargs.pop('fullName', 'testCommittee'),
                delegation_size=kwargs.pop('delegation_size', 10),
                special=kwargs.pop('special', False))
        c.save()
        return c


class TestCountries():
    @staticmethod
    def new_country(**kwargs):
        c = Country(name=kwargs.pop('name', 'TestCountry'),
                    special=kwargs.pop('special', False))
        c.save()
        return c


class TestFiles():
    @staticmethod
    def new_csv(content=[], filename='test.csv'):
        f = StringIO.StringIO()
        f.name = filename

        writer = csv.writer(f)
        for row in content:
            writer.writerow(row)
        f.seek(0)

        return f


