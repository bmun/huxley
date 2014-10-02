# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.db import models


class LineItem(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=128)
    notes = models.TextField(blank=True, default='')
    school = models.ForeignKey('core.School')

    def __unicode__(self):
        return '%s: %s (%d)' % (self.school.name, self.description, self.amount)

    class Meta:
        db_table = 'line_item'
        ordering = ['school']
