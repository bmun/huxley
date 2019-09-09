# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='status_code',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logentry',
            name='uri',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
