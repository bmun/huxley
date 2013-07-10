# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models

from huxley.accounts.constants import *
from huxley.core.models import *

import re

class HuxleyUser(AbstractUser):

    TYPE_ADVISOR = 1
    TYPE_CHAIR = 2
    USER_TYPE_CHOICES = ((TYPE_ADVISOR, 'Advisor'),
                         (TYPE_CHAIR, 'Chair'))

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=TYPE_ADVISOR)
    school = models.OneToOneField(School, related_name='advisor', null=True)  # Advisors only.
    committee = models.ForeignKey(Committee, related_name='chair', null=True) # Chairs only.

    def is_advisor(self):
        return self.user_type == self.TYPE_ADVISOR

    def is_chair(self):
        return self.user_type == self.TYPE_CHAIR

    def default_path(self):
        if self.is_advisor():
            return reverse('advisor_welcome')
        elif self.is_chair():
            return reverse('chair_attendance')

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
        return user.default_path()

    def change_password(self, old, new1, new2):
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
        if not self.check_password(old):
            return False, ChangePasswordErrors.INCORRECT_PASSWORD
        
        self.set_password(new1)
        self.save();
        return True, None

    class Meta:
        db_table = 'huxley_user'
        verbose_name = 'user'
