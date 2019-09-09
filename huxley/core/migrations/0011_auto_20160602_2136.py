# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20160531_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='id',
        ),
        migrations.AlterField(
            model_name='conference',
            name='session',
            field=models.PositiveSmallIntegerField(default=0, serialize=False, primary_key=True),
        ),
    ]
