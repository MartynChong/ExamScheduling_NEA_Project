# Generated by Django 3.0.3 on 2020-08-19 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_populate_access_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='clash_done',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='accountmade',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
