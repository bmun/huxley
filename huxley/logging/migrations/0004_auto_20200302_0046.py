# Generated by Django 2.2.6 on 2020-03-02 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_logentry_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='timestamp'),
        ),
    ]
