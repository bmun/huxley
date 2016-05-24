# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_assignment_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='dual_or_single',
            field=models.PositiveSmallIntegerField(default=2, choices=[(1, b'Single'), (2, b'Double')]),
        ),
        migrations.AlterField(
            model_name='delegate',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='primary_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='school',
            name='secondary_email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
