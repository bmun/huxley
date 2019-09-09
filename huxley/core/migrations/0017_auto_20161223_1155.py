# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20160724_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delegate',
            name='assignment',
            field=models.ForeignKey(related_name='delegates', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.Assignment', null=True),
        ),
    ]
