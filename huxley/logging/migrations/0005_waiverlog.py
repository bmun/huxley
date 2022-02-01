# Generated by Django 2.2.6 on 2022-01-31 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0004_auto_20200302_0046'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaiverLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waiver_unique_id', models.CharField(max_length=64)),
                ('signer_username', models.CharField(max_length=64)),
                ('signer_name', models.CharField(max_length=64)),
                ('signer_email', models.EmailField(max_length=254)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
