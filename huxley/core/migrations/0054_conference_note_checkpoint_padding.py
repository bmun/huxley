# Generated by Django 2.2.6 on 2021-02-27 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20210227_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='note_checkpoint_padding',
            field=models.PositiveIntegerField(default=5000),
        ),
    ]
