# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_assignment_is_double'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='is_double',
            field=models.BooleanField(default=True),
        ),
    ]
