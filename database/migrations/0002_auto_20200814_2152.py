# Generated by Django 3.0.3 on 2020-08-14 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exampupil',
            name='examcode_link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Exam'),
        ),
        migrations.AddField(
            model_name='exampupil',
            name='studentid_link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Student'),
        ),
    ]
