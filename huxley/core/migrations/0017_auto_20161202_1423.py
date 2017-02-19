# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20160724_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='delegate',
            name='session_one',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='delegate',
            name='session_two',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='delegate',
            name='session_three',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='delegate',
            name='session_four',
            field=models.BooleanField(default=False),
        ),
    ]
