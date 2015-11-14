# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import datetime
import json
import logging

from django.test import TestCase

from huxley.logging.handlers import DatabaseHandler
from huxley.logging.models import LogEntry


class LogEntryTestCase(TestCase):
    '''Should successfully create a LogEntry object and save it.'''
    def test_valid(self):
        log_entry = LogEntry.objects.create(
            level='DEBUG',
            message='This is a message',
            timestamp=datetime.datetime(2015, 05, 27),
            uri="/some/random/uri",
            status_code=200,
            username='username')

        self.assertEqual(log_entry.level, 'DEBUG')
        self.assertEqual(log_entry.message, 'This is a message')
        self.assertEqual(log_entry.timestamp, datetime.datetime(2015, 05, 27))
        self.assertEqual(log_entry.uri, "/some/random/uri")
        self.assertEqual(log_entry.status_code, 200)
        self.assertEqual(log_entry.username, 'username')


class DatabaseHandlerTestCase(TestCase):
    '''DatabaseHandler should create a LogEntry object and save it.'''
    def test_valid(self):
        formatter = logging.Formatter('%(asctime)s: %(levelname)s %(message)s')
        message = "There is a problem."
        uri = "/some/random/uri"
        status_code = 400
        username = 'username'
        log_record = logging.makeLogRecord({
                    'name':'huxley.server',
                    'level':10,
                    'fn':'',
                    'lno':'',
                    'msg':json.dumps({
                         'message': message,
                         'uri': uri,
                         'status_code': status_code,
                         'username': username}),
                    'args':(),
                    'exc_info':None})

        handler = DatabaseHandler()
        handler.formatter = formatter
        handler.emit(log_record)

        log_entry = LogEntry.objects.get(id=1)
        self.assertEqual(log_entry.level, log_record.levelname)
        self.assertEqual(log_entry.message, message)
        self.assertEqual(log_entry.timestamp,
            datetime.datetime.strptime(log_record.asctime, "%Y-%m-%d %H:%M:%S,%f"))
        self.assertEqual(log_entry.uri, uri)
        self.assertEqual(log_entry.status_code, status_code)
        self.assertEqual(log_entry.username, username)
