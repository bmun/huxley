# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_school_finalized'),
    ]

    operations = [
        migrations.RenameField(
            model_name='school',
            old_name='finalized',
            new_name='assignments_finalized',
        ),
    ]
