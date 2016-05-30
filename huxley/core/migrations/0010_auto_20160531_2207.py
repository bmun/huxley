# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_conference_external'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='delegate_fee',
            field=models.DecimalField(default=Decimal('50.00'), max_digits=6, decimal_places=2),
        ),
        migrations.AddField(
            model_name='conference',
            name='registration_fee',
            field=models.DecimalField(default=Decimal('50.00'), max_digits=6, decimal_places=2),
        ),
    ]
