# Generated by Django 3.0.7 on 2021-07-05 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0013_applicant_upload_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='skills',
            field=models.TextField(blank=True, null=True),
        ),
    ]
