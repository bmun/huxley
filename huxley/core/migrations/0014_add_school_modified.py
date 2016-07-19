# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_school_waivers_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='modified_at',
            field=models.DateTimeField(default=timezone.now),
        ),
    ]
