# Generated by Django 2.2.6 on 2021-12-28 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_delete_waiver'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autotag', models.CharField(max_length=64)),
                ('username', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('delegate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Delegate')),
            ],
        ),
    ]
