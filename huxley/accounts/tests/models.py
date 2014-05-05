# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.test import TestCase

from huxley.accounts.constants import *
from huxley.accounts.models import *


class HuxleyUserTestCase(TestCase):

    def test_authenticate(self):
        '''It should correctly authenticate and return a user, or return an
        error message.'''
        kunal = HuxleyUser.objects.create(username='kunal', email='kunal@lol.lol')
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
        '''It should correctly change a user's password or return an error.'''
        user = HuxleyUser.objects.create(username='adavis', email='lol@lol.lol')
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
