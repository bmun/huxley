# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from unittest import TestCase

from rest_framework.serializers import ValidationError

from huxley.api import validators


class ValidatorsTestCase(TestCase):

    def run_tests(self, data, func):
        for value, should_pass in data.items():
            if should_pass:
                self.assertEqual(func(value), None)
            else:
                with self.assertRaises(ValidationError):
                    func(value)

    def test_name(self):
        self.run_tests({
            'United States of America': True,
            'St. Kitts': True,
            'Côte d\'Ivoire': True,
            '<> Street': False,
            '<script />': False,
            'Hyphenated-Country': True,
        }, validators.name)

    def test_address(self):
        self.run_tests({
            '22 Jump-Jump St.': True,
        }, validators.address)

    def test_numeric(self):
        self.run_tests({
            '22': True,
            '1 2 3': True,
            '1-3': False,
        }, validators.numeric)

    def test_email(self):
        self.run_tests({
            'basic@example.com': True,
            'e_mail-with+special.chars@example-domain.edu': True,
            'basic@sub.domain.example.org': True,
            'basic@domain-with.special.chars': True,
            '99999': False
        }, validators.email)

    def test_phone_international(self):
        self.run_tests({
            '+1-33343-43434 (32)': True,
            '(111) 111-1111': True,
            '(111) 111-1111 x1234': True,
            '(111) 1a1-1111': False,
            'Leeroy Jenkins': False,
        }, validators.phone_international)

    def test_phone_domestic(self):
        self.run_tests({
            '(111) 111-1111': True,
            '(111) 111-1111 x1234': True,
            '(111) 1a1-1111': False,
            'Leeroy Jenkins': False,
        }, validators.phone_domestic)
