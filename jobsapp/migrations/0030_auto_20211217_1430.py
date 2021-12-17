# Generated by Django 3.0.7 on 2021-12-17 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20211217_0910'),
        ('jobsapp', '0029_auto_20211217_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_poster',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.User'),
        ),
    ]
