# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

from rest_framework.serializers import ValidationError


def alphanumeric(value, field):
    '''Raises a ValidationError if @param 'value' is not alphanumeric.'''
    if re.match("^[A-Za-z0-9\s]+$", value) is None:
        raise ValidationError('%s contains invalid characters.' % field)


def alphabetical(value, field):
    '''Raises a ValidationError if @param 'value' is not alphabetical.'''
    if re.match("^[A-Za-z\s]+$", value) is None:
        raise ValidationError('%s contains invalid characters.' % field)


def numerical(value, field):
    '''Raises a ValidationError if @param 'value' is not numerical.'''
    if re.match("^[0-9\s]+$", value) is None:
        raise ValidationError('%s contains invalid characters.' % field)


def email(value, field):
    '''Raises a ValidationError if @param 'value' is not in email format.'''
    if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value) is None:
        raise ValidationError('%s contains invalid characters.' % field)


def phone_international(value, field):
    '''Raises a ValidationError if @param 'value' is not formatted properly.'''
    if re.match("^[0-9\-x\s\+\(\)]+$", value) is None:
        raise ValidationError('%s contains invalid characters.' % field)


def phone_domestic(value, field):
    '''Raises a ValidationError if @param 'value' is not formatted properly.'''
    if re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", value) is None:
        raise ValidationError('%s contains invalid characters.' % field)
