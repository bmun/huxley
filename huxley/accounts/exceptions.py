# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

class AuthenticationError(LookupError):
    '''Error raised when a user fails to authenticate a User.'''

    INVALID_CREDENTIALS = 'The credentials you provided are invalid.'
    MISSING_FIELDS = 'One or more of the fields is blank.'
    INACTIVE_ACCOUNT = 'Your account is inactive.'

    def __init__(self, message):
        super(AuthenticationError, self).__init__(message)

    @classmethod
    def invalid_credentials(cls):
        return cls(cls.INVALID_CREDENTIALS)

    @classmethod
    def missing_fields(cls):
        return cls(cls.MISSING_FIELDS)

    @classmethod
    def inactive_account(cls):
        return cls(cls.INACTIVE_ACCOUNT)


class PasswordChangeFailed(Exception):
    '''Error raised when a user fails to change their password.'''

    MISSING_FIELDS = 'One or more fields is blank.'
    PASSWORD_TOO_SHORT = 'New password must be at least 6 characters long.'
    INVALID_CHARACTERS = 'New password can only consist of alphanumeric characters and symbols (above numbers).'
    INCORRECT_PASSWORD = 'Incorrect password.'

    def __init__(self, message):
        super(PasswordChangeFailed, self).__init__(message)

    @classmethod
    def missing_fields(cls):
        return cls(cls.MISSING_FIELDS)

    @classmethod
    def password_too_short(cls):
        return cls(cls.PASSWORD_TOO_SHORT)

    @classmethod
    def invalid_characters(cls):
        return cls(cls.INVALID_CHARACTERS)

    @classmethod
    def incorrect_password(cls):
        return cls(cls.INCORRECT_PASSWORD)
