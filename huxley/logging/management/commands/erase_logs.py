# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

from huxley.logging.models import LogEntry

class Command(BaseCommand):
    args = '<days> (optional).'
    help = 'Deletes all log entries after a specified number of days (defaults to 30).'

    def handle(self, *args, **kwargs):
        days = int(args[0]) if args else 30

        cutoff = datetime.now() - timedelta(days=days)
        records = LogEntry.objects.filter(timestamp__lt=cutoff)
        records.delete()

        return

