# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-29 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0027_committee_feedback'), ]

    operations = [
        migrations.AlterField(
            model_name='committeefeedback',
            name='comment',
            field=models.TextField(default=b''), ),
        migrations.AlterField(
            model_name='registration',
            name='committee_preferences',
            field=models.ManyToManyField(
                blank=True, to='core.Committee'), ),
    ]
