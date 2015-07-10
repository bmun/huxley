# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.db import models

class LogEntry(models.Model):
    level = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField('timestamp', null=True, blank=True)

    def __unicode__(self):
        return u'%s: %s' % (self.level, self.timestamp)
