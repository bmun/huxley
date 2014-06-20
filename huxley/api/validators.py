# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

from rest_framework import serializers


def alphanumeric(string, error):
    '''Raises a ValidationError if @param 'string' is not alphanumeric.'''
    if re.match("^[A-Za-z0-9\s]+$", string) is None:
        raise serializers.ValidationError(error+' contains invalid characters.')


def alphabetical(string, error):
    '''Raises a ValidationError if @param 'string' is not alphabetical.'''
    if re.match("^[A-Za-z\s]+$", string) is None:
        raise serializers.ValidationError(error+' contains invalid characters.')


def numerical(string, error):
    '''Raises a ValidationError if @param 'string' is not numerical.'''
    if re.match("^[0-9\s]+$", string) is None:
        raise serializers.ValidationError(error+' contains invalid characters.')


def email(string, error):
    '''Raises a ValidationError if @param 'string' is not in email format.'''
    if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", string) is None:
        raise serializers.ValidationError(error+' contains invalid characters.')


def phone_international(string, error):
    '''Raises a ValidationError if @param 'string' is not formatted properly.'''
    if(not bool(re.match("^[0-9\-x\s\+\(\)]+$", string))):
        raise serializers.ValidationError('%s contains invalid characters.' % error)


def phone_domestic(string, error):
    '''Raises a ValidationError if @param 'string' is not formatted properly.'''
    if(not bool(re.match("^\(?([0-9]{3})\)?\s([0-9]{3})-([0-9]{4})(\sx[0-9]{1,5})?$", string))):
        raise serializers.ValidationError('%s contains invalid characters.' % error)
