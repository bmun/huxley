# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

from huxley.logging.models import LogEntry


class Command(BaseCommand):
    def add_arguments(self, parser):
    	parser.add_argument(
    		'--days',
    		type=int,
    		help='Deletes all log entries after DAYS days where DAYS is \
    		optional (defaults to 30).')

    def handle(self, *args, **options):
        days = options['days'] if options['days'] else 30

        cutoff = datetime.now() - timedelta(days=days)
        records = LogEntry.objects.filter(timestamp__lt=cutoff)
        records.delete()

        return

