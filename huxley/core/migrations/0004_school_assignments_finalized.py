# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_school_chinese_speaking_delegates'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='assignments_finalized',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
