# Generated by Django 3.0.3 on 2020-08-19 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20200819_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='clash_done',
        ),
        migrations.RemoveField(
            model_name='student',
            name='accountmade',
        ),
    ]
