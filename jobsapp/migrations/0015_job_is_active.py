# Generated by Django 3.0.7 on 2021-10-21 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0014_job_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
