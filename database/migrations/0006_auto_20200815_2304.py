# Generated by Django 3.0.3 on 2020-08-15 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20200814_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exampupil',
            name='examcode',
        ),
        migrations.RemoveField(
            model_name='exampupil',
            name='pupilid',
        ),
        migrations.AddField(
            model_name='student',
            name='accesscode',
            field=models.TextField(null=True),
        ),
    ]
