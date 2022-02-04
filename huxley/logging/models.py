# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.db import models


class LogEntry(models.Model):
    level = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField('timestamp', null=True, blank=True)

    uri = models.CharField(max_length=200)
    status_code = models.PositiveSmallIntegerField(default=0)
    username = models.CharField(max_length=200)

    def __str__(self):
        return u'%s: %s' % (self.level, self.timestamp)


class WaiverLog(models.Model):
    waiver_unique_id = models.CharField(max_length=64)
    signer_username = models.CharField(max_length=64)
    signer_name = models.CharField(max_length=64)
    signer_email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s: %s' % (self.signer_username, self.signer_name)
