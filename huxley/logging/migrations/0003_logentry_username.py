# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_auto_20151025_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='username',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
