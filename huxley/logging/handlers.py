# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import datetime
import json
import logging


class DatabaseHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        # Import the model lazily; otherwise it's imported before its AppConfig.
        from huxley.logging.models import LogEntry

        try:
            self.format(record)
            data = json.loads(record.message)
            log_entry = LogEntry(
                level=record.levelname,
                message=data['message'],
                timestamp=datetime.datetime.strptime(record.asctime, "%Y-%m-%d %H:%M:%S,%f"),
                uri=data['uri'],
                status_code=data['status_code'],
                username=data['username'])
            log_entry.save()
        except:
            pass
