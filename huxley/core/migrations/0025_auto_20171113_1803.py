# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-13 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20170927_2010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='fees_owed',
            new_name='delegate_fees_owed',
        ),
        migrations.RenameField(
            model_name='registration',
            old_name='fees_paid',
            new_name='delegate_fees_paid',
        ),
        migrations.AddField(
            model_name='registration',
            name='registration_fee_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registration',
            name='committee_preferences',
            field=models.ManyToManyField(blank=True, null=True, to='core.Committee'),
        ),
    ]
