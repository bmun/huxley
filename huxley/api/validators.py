# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

from django.core.validators import validate_email

from rest_framework import serializers

def validate_alphanumeric(string, error):
    if re.match("^[A-Za-z0-9\s]+$", string) is None:
        raise serializers.ValidationError(error)


def validate_alphabetical(string, error):
    if re.match("^[A-Za-z\s]+$", string) is None:
        return serializers.ValidationError(error)

def validate_numerical(string, error):
    if re.match("^[0-9\s]+$", string) is None:
        return serializers.ValidationError(error)

def validate_email(string, error):
    if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", string) is None:
        return serializers.ValidationError(error)

