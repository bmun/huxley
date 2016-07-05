# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_school_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='delegate_names_finalized',
            field=models.BooleanField(default=False),
        ),
    ]
