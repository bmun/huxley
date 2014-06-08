# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.test import TestCase

from huxley.accounts.constants import *
from huxley.accounts.exceptions import AuthenticationError
from huxley.accounts.models import *


class UserTestCase(TestCase):

    def test_authenticate(self):
        '''It should correctly authenticate and return a user, or return an
        error message.'''
        kunal = User.objects.create(username='kunal', email='kunal@lol.lol')
        kunal.set_password('mehta')
        kunal.is_active = False
        kunal.save()

        def assert_raises(username, password, message):
            with self.assertRaises(AuthenticationError):
                try:
                    User.authenticate(username, password)
                except AuthenticationError as e:
                    self.assertEqual(str(e), message)
                    raise

        assert_raises('kunal', '', AuthenticationError.MISSING_FIELDS)
        assert_raises('', 'mehta', AuthenticationError.MISSING_FIELDS)
        assert_raises('kunal', 'm', AuthenticationError.INVALID_CREDENTIALS)
        assert_raises('k', 'mehta', AuthenticationError.INVALID_CREDENTIALS)
        assert_raises('kunal', 'mehta', AuthenticationError.INACTIVE_ACCOUNT)

        kunal.is_active = True
        kunal.save();

        user = User.authenticate('kunal', 'mehta')
        self.assertEqual(user, kunal)

    def test_change_password(self):
        '''It should correctly change a user's password or return an error.'''
        user = User.objects.create(username='adavis', email='lol@lol.lol')
        user.set_password('mr_davis')

        success, error = user.change_password('', 'lololol', 'lololol')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.MISSING_FIELDS, error)

        success, error = user.change_password('mr_davis', '', 'lololol')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.MISSING_FIELDS, error)

        success, error = user.change_password('mr_davis', 'lololol', '')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.MISSING_FIELDS, error)

        success, error = user.change_password('mr_davis', 'lololol', 'roflrofl')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.MISMATCHED_PASSWORDS, error)

        success, error = user.change_password('mr_davis', 'lol', 'lol')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.PASSWORD_TOO_SHORT, error)

        success, error = user.change_password('mr_davis', 'lololol<', 'lololol<')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.INVALID_CHARACTERS, error)

        success, error = user.change_password('roflrofl', 'lololol', 'lololol')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.INCORRECT_PASSWORD, error)

        success, error = user.change_password('mr_davis', 'lololol', 'lololol')
        self.assertTrue(success)
        self.assertTrue(user.check_password('lololol'))
