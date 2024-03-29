# Generated by Django 3.0.7 on 2021-12-08 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20211208_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='academic_qualification',
            field=models.CharField(choices=[('Full Time', 'full'), ('Part Time', 'part'), ('Freelance', 'freelance')], default='Masters', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='current_salary',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='expected_salary',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='job_preference',
            field=models.CharField(choices=[('Full Time', 'full'), ('Part Time', 'part'), ('Freelance', 'freelance')], default='Full Time', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.CharField(choices=[('Executive Level', '1'), ('Manager Level', '2'), ('Mid Level', '3'), ('Junior Level', '4'), ('Beginner Level', '5')], default='Beginner Level', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_summary',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='terms_and_conditions',
            field=models.BooleanField(default=False),
        ),
    ]
