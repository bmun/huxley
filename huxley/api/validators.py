# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

from rest_framework import serializers

def alphanumeric(string, error):
    if re.match("^[A-Za-z0-9\s]+$", string) is None:
        raise serializers.ValidationError(error+' contains invalid characters.')

def alphabetical(string, error):
    if re.match("^[A-Za-z\s]+$", string) is None:
        raise serializers.ValidationError(error+' contains invalid characters.')

def numerical(string, error):
    if re.match("^[0-9\s]+$", string) is None:
        raise serializers.ValidationError(error+' contains invalid characters.')

def email(string, error):
    if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", string) is None:
        raise serializers.ValidationError(error+' contains invalid characters.')

