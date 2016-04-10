# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import datetime, timedelta
from django.core.management import call_command
from django.test import TestCase

from huxley.logging.models import LogEntry

class EraseLogsTest(TestCase):
    def test_no_args(self):
        '''It erases all logs that exist prior to 30 days ago.'''
        old_log = LogEntry.objects.create(
            level='DEBUG',
            message='This should be deleted by the script.',
            timestamp=datetime.now()-timedelta(days=32))
        recent_log = LogEntry.objects.create(
            level='DEBUG',
            message='This should not be deleted by the script.',
            timestamp=datetime.now()-timedelta(days=29))

        call_command('erase_logs')

        logs = LogEntry.objects.all()
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs[0].level, recent_log.level)
        self.assertEqual(logs[0].message, recent_log.message)
        self.assertEqual(logs[0].timestamp, recent_log.timestamp)

    def test_valid_arg(self):
        '''It erase all logs that exist before the number of days specified.'''
        old_log=LogEntry.objects.create(
            level='DEBUG',
            message='This should be deleted by the script.',
            timestamp=datetime.now()-timedelta(days=10))
        recent_log=LogEntry.objects.create(
            level='DEBUG',
            message='This should not be deleted by the script',
            timestamp=datetime.now()-timedelta(days=4))

        call_command('erase_logs', '7')

        logs = LogEntry.objects.all()
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs[0].level, recent_log.level)
        self.assertEqual(logs[0].message, recent_log.message)
        self.assertEqual(logs[0].timestamp, recent_log.timestamp)
