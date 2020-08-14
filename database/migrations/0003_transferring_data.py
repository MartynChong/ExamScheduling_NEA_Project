from django.db import migrations

def link_exams(apps, schema_editor):
    Exampupil = apps.get_model('database', 'Exampupil')
    Exam = apps.get_model('database', 'Exam')
    Student = apps.get_model('database', 'Student')
    for b in Exampupil.objects.all():
        b.examcode_link = Exam.objects.filter(code=b.examcode).first()
        b.save()
        b.studentid_link = Student.objects.filter(code=b.studentid).first()
        b.save()

class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20200814_2012'),
    ]

    operations = [migrations.RunPython(link_exams),
    ]