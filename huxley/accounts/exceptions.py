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
