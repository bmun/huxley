# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'assignment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=8)),
                ('full_name', models.CharField(max_length=128)),
                ('delegation_size', models.PositiveSmallIntegerField(default=2)),
                ('special', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'committee',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session', models.PositiveSmallIntegerField(default=0)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reg_open', models.DateField()),
                ('early_reg_close', models.DateField()),
                ('reg_close', models.DateField()),
                ('min_attendance', models.PositiveSmallIntegerField(default=0)),
                ('max_attendance', models.PositiveSmallIntegerField(default=0)),
                ('open_reg', models.BooleanField(default=True)),
                ('waitlist_reg', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'conference',
                'get_latest_by': 'start_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('special', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'country',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountryPreference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.PositiveSmallIntegerField()),
                ('country', models.ForeignKey(to='core.Country')),
            ],
            options={
                'ordering': ['-school', 'rank'],
                'db_table': 'country_preference',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Delegate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('summary', models.TextField(default=b'', null=True)),
                ('assignment', models.ForeignKey(related_name='delegates', to='core.Assignment')),
            ],
            options={
                'ordering': ['assignment__country'],
                'db_table': 'delegate',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('registered', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('state', models.CharField(max_length=16)),
                ('zip_code', models.CharField(max_length=16)),
                ('country', models.CharField(max_length=64)),
                ('primary_name', models.CharField(max_length=128)),
                ('primary_gender', models.PositiveSmallIntegerField(default=4, choices=[(1, b'Male'), (2, b'Female'), (3, b'Other'), (4, b'Unspecified')])),
                ('primary_email', models.EmailField(max_length=75)),
                ('primary_phone', models.CharField(max_length=32)),
                ('primary_type', models.PositiveSmallIntegerField(default=2, choices=[(2, b'Faculty'), (1, b'Student')])),
                ('secondary_name', models.CharField(max_length=128, blank=True)),
                ('secondary_gender', models.PositiveSmallIntegerField(default=4, blank=True, choices=[(1, b'Male'), (2, b'Female'), (3, b'Other'), (4, b'Unspecified')])),
                ('secondary_email', models.EmailField(max_length=75, blank=True)),
                ('secondary_phone', models.CharField(max_length=32, blank=True)),
                ('secondary_type', models.PositiveSmallIntegerField(default=2, blank=True, choices=[(2, b'Faculty'), (1, b'Student')])),
                ('program_type', models.PositiveSmallIntegerField(default=1, choices=[(1, b'Club'), (2, b'Class')])),
                ('times_attended', models.PositiveSmallIntegerField(default=0)),
                ('international', models.BooleanField(default=False)),
                ('waitlist', models.BooleanField(default=False)),
                ('beginner_delegates', models.PositiveSmallIntegerField()),
                ('intermediate_delegates', models.PositiveSmallIntegerField()),
                ('advanced_delegates', models.PositiveSmallIntegerField()),
                ('spanish_speaking_delegates', models.PositiveSmallIntegerField()),
                ('prefers_bilingual', models.BooleanField(default=False)),
                ('prefers_specialized_regional', models.BooleanField(default=False)),
                ('prefers_crisis', models.BooleanField(default=False)),
                ('prefers_alternative', models.BooleanField(default=False)),
                ('prefers_press_corps', models.BooleanField(default=False)),
                ('registration_comments', models.TextField(default=b'', blank=True)),
                ('fees_owed', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('fees_paid', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('countrypreferences', models.ManyToManyField(to='core.Country', through='core.CountryPreference')),
            ],
            options={
                'db_table': 'school',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='countrypreference',
            name='school',
            field=models.ForeignKey(to='core.School'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='countrypreference',
            unique_together=set([('country', 'school')]),
        ),
        migrations.AddField(
            model_name='committee',
            name='countries',
            field=models.ManyToManyField(to='core.Country', through='core.Assignment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='committee',
            field=models.ForeignKey(to='core.Committee'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='country',
            field=models.ForeignKey(to='core.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='school',
            field=models.ForeignKey(default=None, blank=True, to='core.School', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([('committee', 'country')]),
        ),
    ]
