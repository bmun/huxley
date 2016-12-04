# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0016_auto_20160724_2344'), ]

    operations = [
        migrations.AddField(
            model_name='delegate',
            name='friday_attendance',
            field=models.BooleanField(default=False), ),
        migrations.AddField(
            model_name='delegate',
            name='saturday_afternoon_attendance',
            field=models.BooleanField(default=False), ),
        migrations.AddField(
            model_name='delegate',
            name='saturday_morning_attendance',
            field=models.BooleanField(default=False), ),
        migrations.AddField(
            model_name='delegate',
            name='sunday_attendance',
            field=models.BooleanField(default=False), ),
    ]
