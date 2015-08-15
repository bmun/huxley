# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json, logging

class ExceptionLoggerMiddleware(object):
    def process_exception(self, request, exception):
        logger = logging.getLogger('huxley')
        logger.exception(exception)

class ServerLoggingMiddleware(object):
    def process_exception(self, request, exception):
        logger = logging.getLogger('huxley.server')
        logger.exception(exception)

class LoggingMiddleware(object):
    def process_response(self, request, response):
        if 'api' in request.path:
            logger = logging.getLogger('huxley.api')
            log = json.dumps({
                  'message': "Logging response from the api.",
                  'uri': request.path,
                  'status_code': response.status_code})
            logger.info(log)

        return response
