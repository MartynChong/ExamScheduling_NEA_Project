# Generated by Django 3.0.3 on 2020-08-15 15:05

from django.db import migrations
from database.models import Student

def populate_access_code(apps, schema_editor):
    Students = apps.get_model('database', 'Student')
    count = -1
    StudentList = Student.generate_access_code() 
    for student in Students.objects.all():
        count = count + 1
        student.accesscode = StudentList[count]
        student.save()


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20200815_2304'),
    ]

    operations = [
        migrations.RunPython(populate_access_code)
    ]
