# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import datetime

from django.test import TestCase

from huxley.logs.models import LogEntry

class LogEntryTestCase(TestCase):
    def test_valid(self):
        log_entry = LogEntry.objects.create(
            level='DEBUG',
            message='This is a message',
            timestamp=datetime.datetime(2015,05,27))

        self.assertEqual(log_entry.level, 'DEBUG')
        self.assertEqual(log_entry.message, 'This is a message')
        self.assertEqual(log_entry.timestamp, datetime.datetime(2015,05,27))
