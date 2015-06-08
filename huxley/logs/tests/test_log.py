# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import datetime
import logging

from django.test import TestCase

from huxley.logs.handlers import DatabaseHandler
from huxley.logs.models import LogEntry


class LogEntryTestCase(TestCase):
    '''Should successfully create a LogEntry object and save it.'''
    def test_valid(self):
        log_entry = LogEntry.objects.create(
            level='DEBUG',
            message='This is a message',
            timestamp=datetime.datetime(2015, 05, 27))

        self.assertEqual(log_entry.level, 'DEBUG')
        self.assertEqual(log_entry.message, 'This is a message')
        self.assertEqual(log_entry.timestamp, datetime.datetime(2015, 05, 27))


class DatabaseHandlerTestCase(TestCase):
    '''DatabaseHandler should create a LogEntry object and save it.'''
    def test_valid(self):
        formatter = logging.Formatter('%(asctime)s: %(levelname)s %(message)s')
        log_record = logging.makeLogRecord({
                    'name':'huxley.server',
                    'level':10,
                    'fn':'',
                    'lno':'',
                    'msg':'There is a problem.',
                    'args':(),
                    'exc_info':None})

        handler = DatabaseHandler()
        handler.formatter = formatter
        handler.emit(log_record)

        log_entry = LogEntry.objects.get(id=1)
        self.assertEqual(log_entry.level, log_record.levelname)
        self.assertEqual(log_entry.message, log_record.message)
        self.assertEqual(log_entry.timestamp,
            datetime.datetime.strptime(log_record.asctime, "%Y-%m-%d %H:%M:%S,%f"))
