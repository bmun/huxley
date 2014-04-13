# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django import template
register = template.Library()

@register.filter
def leading_zeros(value, digits):
    """ Pads value with leading zeros, given by digits. """
    try:
        value = str(value)
        for i in range(0, int(digits) - len(value)):
            value = "0" + value
        return value
    except:
        return ""
