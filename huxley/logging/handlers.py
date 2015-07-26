# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import datetime
import logging


class DatabaseHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        # Import the model lazily; otherwise it's imported before its AppConfig.
        from huxley.logging.models import LogEntry

        try:
            self.format(record)
            log_entry = LogEntry(
                level=record.levelname,
                message=record.message,
                timestamp=datetime.datetime.strptime(record.asctime, "%Y-%m-%d %H:%M:%S,%f"))
            log_entry.save()
        except:
            pass
