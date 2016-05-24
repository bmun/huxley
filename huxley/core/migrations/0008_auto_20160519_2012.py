# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160519_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='double',
        ),
        migrations.AddField(
            model_name='assignment',
            name='is_double',
            field=models.BooleanField(default=True),
        ),
    ]
