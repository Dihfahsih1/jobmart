# Generated by Django 3.0.7 on 2021-12-11 10:07

from django.db import migrations
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0017_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=djrichtextfield.models.RichTextField(),
        ),
    ]
