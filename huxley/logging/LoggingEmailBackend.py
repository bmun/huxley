# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json, logging

from django.core.mail.backends import dummy, smtp
from django.db import transaction

from smtplib import SMTPException


class DevLoggingEmailBackend(dummy.EmailBackend):

    def send_messages(self, email_messages):
        logger = logging.getLogger('huxley.api')
        for email in email_messages:
            recipients = email.to[0] if len(email.to) == 1 else ', '.join(email.to)
            log = json.dumps({
              'message': "Sending email",
              'uri': str(recipients),
              'status_code': 0,
              'username': ''})
            logger.info(log)


class LoggingEmailBackend(smtp.EmailBackend):

    def send_messages(self, email_messages):
        logger = logging.getLogger('huxley.api')
        exc_logger = logging.getLogger('huxley.exception')

        with transaction.atomic():
            for email in email_messages:
                recipients = email.to[0] if len(email.to) == 1 else ', '.join(email.to)
                log = json.dumps({
                  'message': "Sending email",
                  'uri': str(recipients),
                  'status_code': 0,
                  'username': ''})
                logger.info(log)

                return super(LoggingEmailBackend, self)._send(email)
