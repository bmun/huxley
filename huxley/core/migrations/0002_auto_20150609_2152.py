# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='prefers_alternative',
        ),
        migrations.RemoveField(
            model_name='school',
            name='prefers_bilingual',
        ),
        migrations.RemoveField(
            model_name='school',
            name='prefers_crisis',
        ),
        migrations.RemoveField(
            model_name='school',
            name='prefers_press_corps',
        ),
        migrations.RemoveField(
            model_name='school',
            name='prefers_specialized_regional',
        ),
        migrations.AddField(
            model_name='school',
            name='committeepreferences',
            field=models.ManyToManyField(to='core.Committee'),
            preserve_default=True,
        ),
    ]
