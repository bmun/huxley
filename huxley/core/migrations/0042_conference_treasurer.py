# Generated by Django 2.2.6 on 2020-08-20 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20200817_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='treasurer',
            field=models.CharField(default='Vishnu Arul', max_length=128),
            preserve_default=False,
        ),
    ]