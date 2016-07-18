# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_school_waivers_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='modified',
            field=models.DateTimeField(default=datetime.utcnow),
        ),
    ]
