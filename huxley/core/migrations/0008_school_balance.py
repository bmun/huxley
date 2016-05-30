# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_school_total_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='balance',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=6, decimal_places=2),
        ),
    ]
