# Generated by Django 3.0.7 on 2021-12-17 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0024_job_skill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='skill',
        ),
        migrations.CreateModel(
            name='JobSkillset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobsapp.Job')),
            ],
        ),
    ]
