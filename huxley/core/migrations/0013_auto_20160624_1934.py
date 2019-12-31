# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_school_balance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delegate',
            options={'ordering': ['school']},
        ),
        migrations.AddField(
            model_name='delegate',
            name='school',
            field=models.ForeignKey(related_name='delegates', to='core.School', null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='delegate',
            name='assignment',
            field=models.ForeignKey(related_name='delegates', blank=True, to='core.Assignment', on_delete=models.SET_NULL),
        ),
        migrations.AlterField(
            model_name='delegate',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
