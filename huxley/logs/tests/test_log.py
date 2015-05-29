# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import datetime
import logging

from django.test import TestCase

from huxley.logs.handlers import DatabaseHandler
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

class DatabaseHanlderTestCase(TestCase):
    def test_valid(self):
        log_record = logging.LogRecord(
            name='Logger',
            level=10,
            pathname='',
            lineno='',
            msg='There is a problem.',
            args=(),
            exc_info=None,
            func=None)

        handler = DatabaseHandler()
        handler.emit(log_record)

        log_entry = LogEntry.objects.get(id=1)
        self.assertEqual(log_entry.level, log_record.levelname)
        self.assertEqual(log_entry.message, log_record.message)
        self.assertEqual(log_entry.timestamp, None)
