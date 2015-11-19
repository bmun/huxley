# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_school_assignments_finalized'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='rejected',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
