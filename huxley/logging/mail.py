# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json, logging

from django.core.mail.backends import dummy, smtp
from django.db import transaction


class DevLoggingEmailBackend(dummy.EmailBackend):

    def send_messages(self, email_messages):
        for email in email_messages:
            log_email(email)


class LoggingEmailBackend(smtp.EmailBackend):

    def send_messages(self, email_messages):
        with transaction.atomic():
            for email in email_messages:
                log_email(email)

                return super(LoggingEmailBackend, self)._send(email)


def log_email(email):
    logger = logging.getLogger('huxley.api')

    recipients = ', '.join(email.to)
    log = json.dumps({
        'message': "Sending email",
        'uri': recipients,
        'status_code': 0,
        'username': ''})
    logger.info(log)
