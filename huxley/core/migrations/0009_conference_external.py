# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_school_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='external',
            field=models.CharField(default='Rita Hu', max_length=128),
            preserve_default=False,
        ),
    ]
