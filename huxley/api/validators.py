# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

# -*- coding: utf-8 -*-

import re

from rest_framework.serializers import ValidationError


def name(value):
    '''Matches names of people, countries and and other things.'''
    if re.match(r'^[A-Za-z\s\.\-\'àèéìòóôù]+$', value) is None:
        raise ValidationError('This field contains invalid characters.')


def address(value):
    '''Matches street addresses.'''
    if re.match(r'^[\w\s\.\-\'àèéìòóôù]+$', value) is None:
        raise ValidationError('This field contains invalid characters.')


def numeric(value):
    '''Matches numbers and spaces.'''
    if re.match(r'^[\d\s]+$', value) is None:
        raise ValidationError('This field can only contain numbers and spaces.')


def email(value):
    '''Loosely matches email addresses.'''
    if re.match(r'^[\w_.+-]+@[\w-]+\.[\w\-.]+$', value) is None:
        raise ValidationError('This is an invalid email address.')


def phone_international(value):
    '''Loosely matches phone numbers.'''
    if re.match(r'^[\d\-x\s\+\(\)]+$', value) is None:
        raise ValidationError('This is an invalid phone number.')


def phone_domestic(value):
    '''Matches domestic phone numbers.'''
    if re.match(r'^\(?(\d{3})\)?\s(\d{3})-(\d{4})(\sx\d{1,5})?$', value) is None:
        raise ValidationError('This is an invalid phone number.')

def nonempty(value):
    '''Requires that a field be non-empty.'''
    if not value:
        raise ValidationError('This field is required.')
