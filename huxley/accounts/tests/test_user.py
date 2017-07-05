# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.test import TestCase

from huxley.accounts.exceptions import AuthenticationError, PasswordChangeFailed
from huxley.accounts.models import User
from huxley.utils.test import models


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
        assert_raises('kunal', 'mehta', AuthenticationError.INVALID_CREDENTIALS)

        kunal.is_active = True
        kunal.save()

        user = User.authenticate('kunal', 'mehta')
        self.assertEqual(user, kunal)

    def test_change_password(self):
        '''It should correctly change a user's password or raise an error.'''
        user = User.objects.create(username='adavis', email='lol@lol.lol')
        user.set_password('old&busted')
        user.save()

        def assert_raises(old_password, new_password, message):
            with self.assertRaises(PasswordChangeFailed):
                try:
                    user.change_password(old_password, new_password)
                except PasswordChangeFailed as e:
                    self.assertEqual(str(e), message)
                    self.assertTrue(user.check_password('old&busted'))
                    raise

        assert_raises('', 'newhotness',
                      PasswordChangeFailed.MISSING_FIELDS)
        assert_raises('old&busted', '',
                      PasswordChangeFailed.MISSING_FIELDS)
        assert_raises('old&busted', 'a',
                      PasswordChangeFailed.PASSWORD_TOO_SHORT)
        assert_raises('old&busted', 'invalid>hotness',
                      PasswordChangeFailed.INVALID_CHARACTERS)
        assert_raises('wrong&busted', 'newhotness',
                      PasswordChangeFailed.INCORRECT_PASSWORD)

        user.change_password('old&busted', 'newhotness')
        self.assertTrue(user.check_password('newhotness'))

    def test_reset_password(self):
        '''It should correctly reset a user's password or raise an error.'''
        password = 'password'
        user = models.new_user(username='lololol', password=password)
        self.assertTrue(user.check_password(password))

        User.reset_password('lololol')
        user = User.objects.get(id=user.id)
        self.assertFalse(user.check_password(password))

        with self.assertRaises(User.DoesNotExist):
            models.new_user(username='', email='')
            User.reset_password('')
