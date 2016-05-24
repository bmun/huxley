# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20160519_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='is_double',
        ),
    ]
