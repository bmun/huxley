# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150609_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='chinese_speaking_delegates',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
