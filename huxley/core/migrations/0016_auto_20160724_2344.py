# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delegate',
            name='assignment',
            field=models.ForeignKey(related_name='delegates', blank=True, to='core.Assignment', null=True),
        ),
        migrations.AlterField(
            model_name='delegate',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='delegate',
            name='summary',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
    ]
