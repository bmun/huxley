# Generated by Django 2.2.6 on 2022-01-16 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_conference_advisor_edit_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]