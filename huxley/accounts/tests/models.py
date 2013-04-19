# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django.contrib.auth.models import User
from django.test import TestCase

from huxley.accounts.constants import *
from huxley.accounts.models import *

class HuxleyUserTest(TestCase):

    def test_authenticate(self):
        """ Tests that the function correctly authenticates and returns a
            user, or returns an error message. """
        kunal = User.objects.create(username='kunal', email='kunal@lol.lol')
        kunal.set_password('kunalmehta')
        kunal.save()

        user, error = HuxleyUser.authenticate('kunal', '')
        self.assertIsNone(user)
        self.assertEqual(error, AuthenticationErrors.MISSING_FIELDS)

        user, error = HuxleyUser.authenticate('', 'kunalmehta')
        self.assertIsNone(user)
        self.assertEqual(error, AuthenticationErrors.MISSING_FIELDS)

        user, error = HuxleyUser.authenticate('roflrofl', 'roflrofl')
        self.assertIsNone(user)
        self.assertEqual(error, AuthenticationErrors.INVALID_LOGIN)

        user, error = HuxleyUser.authenticate('kunal', 'kunalmehta')
        self.assertEqual(user, kunal)
        self.assertIsNone(error)

    def test_change_password(self):
        """ Tests that the function correctly changes a user's password, or
            returns an error message. """
        user = User.objects.create(username='adavis', email='lol@lol.lol')
        user.set_password('mr_davis')

        success, error = HuxleyUser.change_password(user, '', 'lololol', 'lololol')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.MISSING_FIELDS, error)

        success, error = HuxleyUser.change_password(user, 'mr_davis', '', 'lololol')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.MISSING_FIELDS, error)

        success, error = HuxleyUser.change_password(user, 'mr_davis', 'lololol', '')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.MISSING_FIELDS, error)

        success, error = HuxleyUser.change_password(user, 'mr_davis', 'lololol', 'roflrofl')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.MISMATCHED_PASSWORDS, error)

        success, error = HuxleyUser.change_password(user, 'mr_davis', 'lol', 'lol')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.PASSWORD_TOO_SHORT, error)

        success, error = HuxleyUser.change_password(user, 'mr_davis', 'lololol<', 'lololol<')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.INVALID_CHARACTERS, error)

        success, error = HuxleyUser.change_password(user, 'roflrofl', 'lololol', 'lololol')
        self.assertFalse(success)
        self.assertEquals(ChangePasswordErrors.INCORRECT_PASSWORD, error)

        success, error = HuxleyUser.change_password(user, 'mr_davis', 'lololol', 'lololol')
        self.assertTrue(success)
        self.assertTrue(user.check_password('lololol'))