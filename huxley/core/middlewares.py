# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json, logging, sys, traceback


class ExceptionLoggerMiddleware(object):

    def process_exception(self, request, exception):
        logger = logging.getLogger('huxley.exception')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        log = json.dumps({
              'message': exc_traceback,
              'uri': request.path,
              'status_code': 500,
              'username': request.user.username})
        logger.exception(log)


class LoggingMiddleware(object):

    def process_response(self, request, response):
        if 'api' in request.path:
            logger = logging.getLogger('huxley.api')
            log = json.dumps({
                  'message': "",
                  'uri': request.path,
                  'status_code': response.status_code,
                  'username': request.user.username})
            logger.info(log)

        return response
