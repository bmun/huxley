# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160527_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='total_fees',
        ),
    ]
