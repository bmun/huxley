# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django import template
register = template.Library()

@register.filter
def is_advisor(user):
    try:
        return user.is_advisor()
    except:
        return False

@register.filter
def is_chair(user):
    try:
        return user.is_chair()
    except:
        return False
