# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160519_1752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='dual_or_single',
            new_name='double',
        ),
    ]
