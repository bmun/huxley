# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from huxley.accounts.constants import *
from huxley.core.models import *

import re

class HuxleyUser(User):
    """ A proxy model to add extra functionality to the default django
        User model. This will eventually be changed to become the default
        User model for the application, and the static methods will become
        instance methods. """
    
    @staticmethod
    def authenticate(username, password):
        """ Attempts to authenticate a user, given a username and password.
            Returns a 2-tuple of (User) user, (str) error. """
        if not (username and password):
            return None, AuthenticationErrors.MISSING_FIELDS

        user = authenticate(username=username, password=password)
        if user is None:
            return None, AuthenticationErrors.INVALID_LOGIN
        if not user.is_active:
            return None, AuthenticationErrors.INACTIVE_ACCOUNT

        return user, None

    @staticmethod
    def login(request, user):
        """ Logs in a user and returns a redirect url based on whether they're
            an advisor or chair. """
        login(request, user)
        if SecretariatProfile.objects.filter(user=user).exists():
            return reverse('chair_attendance')
        else:
            return reverse('advisor_welcome')

    @staticmethod
    def change_password(user, old, new1, new2):
        """ Attempts to change the given user's password. Returns a 2-tuple
            of (bool) success, (str) error. """
        if not (old and new1 and new2):
            return False, ChangePasswordErrors.MISSING_FIELDS
        if new1 != new2:
            return False, ChangePasswordErrors.MISMATCHED_PASSWORDS
        if len(new1) < 6:
            return False, ChangePasswordErrors.PASSWORD_TOO_SHORT
        if not re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", new1):
            return False, ChangePasswordErrors.INVALID_CHARACTERS
        if not user.check_password(old):
            return False, ChangePasswordErrors.INCORRECT_PASSWORD
        
        user.set_password(new1)
        user.save();
        return True, None

    class Meta:
        proxy = True