# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_assignment_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='total_fees',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=6, decimal_places=2),
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
