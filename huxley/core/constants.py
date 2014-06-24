# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json


class Constants():
    '''Base class that allows constants to be serialized to JSON.'''

    @classmethod
    def to_dict(cls):
        return {k: v for k, v in vars(cls).items() if not k.startswith('__')}

    @classmethod
    def to_json(cls):
        return json.dumps(cls.to_dict())


class ContactGender(Constants):
    '''Gender of a school's primary/secondary contacts.'''
    MALE = 1
    FEMALE = 2
    OTHER = 3
    UNSPECIFIED = 4


class ContactType(Constants):
    '''Whether a school's primary/secondary contact is a student or faculty.'''
    STUDENT = 1
    FACULTY = 2


class ProgramTypes(Constants):
    '''Type of a school's MUN program.'''
    CLUB = 1
    CLASS = 2
