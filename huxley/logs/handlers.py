# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import datetime
import logging

from huxley.logs.models import LogEntry


class DatabaseHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        try:
            log_entry = LogEntry(
                level=record.levelname,
                message=record.msg,
                timestamp=datetime.datetime.now())
            log_entry.save()
        except:
            pass
