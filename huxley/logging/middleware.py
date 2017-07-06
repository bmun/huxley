# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json, logging, sys, traceback


class ExceptionLoggerMiddleware(object):

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    return self.get_response(request)

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

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)

    if 'api' in request.path:
      logger = logging.getLogger('huxley.api')
      status_code = response.status_code
      message = response.getvalue() if 500 > status_code >= 400 else ""
      log = json.dumps({
            'message': message,
            'uri': request.path,
            'status_code': status_code,
            'username': request.user.username})
      logger.info(log)

    return response
