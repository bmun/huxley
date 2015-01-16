# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import logging

class ExceptionLoggerMiddleware(object):
    def process_exception(self, request, exception):
        logger = logging.getLogger('huxley')
        logger.critical(exception)
