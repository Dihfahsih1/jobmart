# Generated by Django 3.0.7 on 2021-12-17 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0026_auto_20211217_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='company_description',
        ),
        migrations.RemoveField(
            model_name='job',
            name='company_name',
        ),
    ]
