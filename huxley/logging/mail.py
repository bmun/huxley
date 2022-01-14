# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json, logging, sys, traceback

from django.core.mail.backends import dummy, smtp
from django.db import transaction

from smtplib import SMTPException


class DevLoggingEmailBackend(dummy.EmailBackend):

    def send_messages(self, email_messages):
        for email in email_messages:
            log_email(email)


class LoggingEmailBackend(smtp.EmailBackend):

    def send_messages(self, email_messages):
        with transaction.atomic():
            for email in email_messages:
                log_email(email)

                try:
                    return super(LoggingEmailBackend, self).send_messages([email])
                except SMTPException:
                    logger = logging.getLogger('huxley.api')
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    exc_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                    log = json.dumps({
                          'message': exc_traceback,
                          'uri': ', '.join(email.to),
                          'status_code': 500,
                          'username': ''})
                    logger.exception(log)


def log_email(email):
    logger = logging.getLogger('huxley.api')

    recipients = ', '.join(email.to)
    log = json.dumps({
        'message': "Sending email",
        'uri': recipients,
        'status_code': 0,
        'username': ''})
    logger.info(log)
