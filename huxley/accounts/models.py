# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.db import models

from huxley.accounts.exceptions import AuthenticationError, PasswordChangeFailed
from huxley.core.models import Committee, School


class User(AbstractUser):

    TYPE_ADVISOR = 1
    TYPE_CHAIR = 2
    TYPE_DELEGATE = 3
    USER_TYPE_CHOICES = ((TYPE_ADVISOR, 'Advisor'),
                         (TYPE_CHAIR, 'Chair'),
                         (TYPE_DELEGATE, 'Delegate'))

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=TYPE_ADVISOR)
    school = models.OneToOneField(School, related_name='advisor', null=True, blank=True)  # Advisors and Delegate.
    committee = models.ForeignKey(Committee, related_name='chair', null=True, blank=True) # Chairs and Delegate.

    def is_advisor(self):
        return self.user_type == self.TYPE_ADVISOR

    def is_chair(self):
        return self.user_type == self.TYPE_CHAIR

    def is_delegate(self):
        return self.user_type == self.TYPE_DELEGATE

    @staticmethod
    def authenticate(username, password):
        '''Attempt to authenticate a user, given a username (or email) and
        password. Return the user or raise AuthenticationError.'''
        if not (username and password):
            raise AuthenticationError.missing_fields()

        user = authenticate(username=username, password=password)
        if user is None:
            try:
                u = User.objects.get(email=username)
                user = authenticate(username=u.username, password=password)
            except User.DoesNotExist:
                pass

        if user is None:
            raise AuthenticationError.invalid_credentials()
        if not user.is_active:
            raise AuthenticationError.inactive_account()

        return user

    @classmethod
    def reset_password(cls, username):
        '''Reset a user's password and email it to them, or raise if the
        user doesn't exist.'''
        if not username:
            raise User.DoesNotExist

        query = models.Q(username=username) | models.Q(email=username)
        user = cls.objects.get(query)

        new_password = cls.objects.make_random_password(length=10)
        user.set_password(new_password)
        user.save()

        user.email_user('Huxley Password Reset',
                        'Your password has been reset to %s.\n'
                        'Thank you for using Huxley!' % (new_password),
                        from_email='no-reply@bmun.org')

    def change_password(self, old_password, new_password):
        '''Change the user's password, or raise PasswordChangeFailed.'''
        valid_regex = "^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$"

        if not (old_password and new_password):
            raise PasswordChangeFailed.missing_fields()
        if len(new_password) < 6:
            raise PasswordChangeFailed.password_too_short()
        if not re.match(valid_regex, new_password):
            raise PasswordChangeFailed.invalid_characters()
        if not self.check_password(old_password):
            raise PasswordChangeFailed.incorrect_password()

        self.set_password(new_password)
        self.save()

    class Meta:
        db_table = u'user'
