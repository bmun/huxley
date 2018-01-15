# Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import uuid

from django.conf import settings
from django.core.exceptions import PermissionDenied

from huxley.accounts.models import User
from huxley.core.constants import ContactGender, ContactType, ProgramTypes

from huxley.core.models import School, Committee, CommitteeFeedback, Country, Delegate, Assignment, Registration, Conference, PositionPaper, Rubric

if not settings.TESTING:
    raise PermissionDenied


def new_user(**kwargs):
    username = kwargs.pop('username', None) or str(uuid.uuid4())
    u = User(username=username, email=kwargs.pop('email', 'test@user.in'))

    password = kwargs.pop('password', 'test')
    u.set_password(password)
    u.PASSWORD_FOR_TESTS_ONLY = password

    u.first_name = kwargs.pop('first_name', 'Test')
    u.last_name = kwargs.pop('last_name', 'User')

    for attr, value in kwargs.items():
        setattr(u, attr, value)

    u.save()
    return u


def new_superuser(*args, **kwargs):
    kwargs['is_superuser'] = True
    kwargs['is_staff'] = True
    return new_user(**kwargs)


def new_school(**kwargs):
    s = School(
        name=kwargs.pop('name', 'Test School'),
        address=kwargs.pop('address', '1 Schoolhouse Road'),
        city=kwargs.pop('city', 'Berkeley'),
        state=kwargs.pop('state', 'CA'),
        zip_code=kwargs.pop('zip_code', '94024'),
        country=kwargs.pop('country', 'United States of America'),
        primary_name=kwargs.pop('primary_name', 'first'),
        primary_gender=kwargs.pop('primary_gender', ContactGender.MALE),
        primary_email=kwargs.pop('primary_email', 'e@mail.com'),
        primary_phone=kwargs.pop('primary_phone', '1234567890'),
        primary_type=kwargs.pop('primary_type', ContactType.FACULTY),
        secondary_name=kwargs.pop('secondary_name', ''),
        secondary_gender=kwargs.pop('secondary_gender', ContactGender.MALE),
        secondary_email=kwargs.pop('secondary_email', ''),
        secondary_phone=kwargs.pop('secondary_phone', ''),
        secondary_type=kwargs.pop('secondary_type', ContactType.FACULTY),
        program_type=kwargs.pop('program_type', ProgramTypes.CLUB),
        times_attended=kwargs.pop('times_attended', 0))

    user = kwargs.pop('user', None)
    for attr, value in kwargs.items():
        setattr(s, attr, value)

    s.save()

    if user is None:
        committee = new_committee()
        new_user(username=str(uuid.uuid4()), school=s, committee=committee)
    else:
        user.school = s
        user.save()

    return s


def new_committee(**kwargs):
    c = Committee(
        name=kwargs.pop('name', 'testCommittee'),
        full_name=kwargs.pop('fullName', 'testCommittee'),
        delegation_size=kwargs.pop('delegation_size', 10),
        special=kwargs.pop('special', False))
    c.save()

    user = kwargs.pop('user', None)
    for attr, value in kwargs.items():
        setattr(c, attr, value)

    c.save()

    if user is None:
        new_user(
            username=str(uuid.uuid4()), committee=c, user_type=User.TYPE_CHAIR)
    else:
        user.committee = c
        user.save()
    return c


def new_committee_feedback(**kwargs):
    committee = new_committee()
    feedback = CommitteeFeedback(
        committee=kwargs.pop('committee', committee),
        comment=kwargs.pop('comment', "Daddy Nikhil though"))
    feedback.save()
    return feedback


def new_country(**kwargs):
    c = Country(
        name=kwargs.pop('name', 'TestCountry'),
        special=kwargs.pop('special', False))
    c.save()
    return c


def new_delegate(**kwargs):
    a = kwargs.pop('assignment', None) or new_assignment()
    s = kwargs.pop('school', None) or a.registration.school
    user = kwargs.pop('user', None)

    d = Delegate(
        assignment=a,
        school=s,
        name=kwargs.pop('name', 'Nate Parke'),
        email=kwargs.pop('email', 'nate@earthlink.gov'),
        summary=kwargs.pop('summary', 'He did well!'), )
    d.save()

    if user:
        user.delegate = d
        user.save()
    return d


def new_assignment(**kwargs):
    test_committee = kwargs.pop('committee', None) or new_committee()
    test_registration = kwargs.pop('registration', None) or new_registration()
    test_country = kwargs.pop('country', None) or new_country()
    test_paper = kwargs.pop('paper', None)

    a = Assignment(
        committee=test_committee,
        registration=test_registration,
        country=test_country,
        paper=test_paper,
        rejected=kwargs.pop('rejected', False), )
    a.save()
    return a


def new_registration(**kwargs):
    test_school = kwargs.pop('school', None) or new_school()
    test_conference = kwargs.pop('conference',
                                 None) or Conference.get_current()
    r = Registration(
        school=test_school,
        conference=test_conference,
        num_beginner_delegates=kwargs.pop('num_beginner_delegates', 0),
        num_intermediate_delegates=kwargs.pop('num_intermediate_delegates', 0),
        num_advanced_delegates=kwargs.pop('num_advanced_delegates', 0),
        num_spanish_speaking_delegates=kwargs.pop(
            'num_spanish_speaking_delegates', 0),
        num_chinese_speaking_delegates=kwargs.pop(
            'num_chinese_speaking_delegates', 0))

    r.save()

    return r


def new_position_paper(**kwargs):
    p = PositionPaper()
    p.save()
    return p


def new_rubric(**kwargs):
    r = Rubric()
    r.save()
    return r
