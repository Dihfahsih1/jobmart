# Generated by Django 3.0.7 on 2021-12-17 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0028_auto_20211217_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='user',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]