# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=128)),
                ('notes', models.TextField(default=b'', blank=True)),
                ('school', models.ForeignKey(to='core.School')),
            ],
            options={
                'ordering': ['school'],
                'db_table': 'line_item',
            },
            bases=(models.Model,),
        ),
    ]
