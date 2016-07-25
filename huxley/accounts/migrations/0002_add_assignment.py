# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='assignment',
            field=models.ForeignKey(related_name='delegate', blank=True, to='core.Assignment', null=True),
        ),
    ]
