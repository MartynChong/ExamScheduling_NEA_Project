from django.db import models
import random, string

class Exam(models.Model):
    subject = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    code = models.TextField(primary_key=True, blank=True)
    date = models.TextField(blank=True, null=True)
    times = models.TextField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Exam'
    
        

class Student(models.Model):
    studentid = models.TextField(primary_key=True, blank=True)
    firstname = models.TextField(blank=True, null=True)
    lastname = models.TextField(blank=True, null=True)
    birthdate = models.TextField(blank=True, null=True)
    accessarrangement = models.TextField(blank=True, null=True)
    accesscode = models.TextField(null = True)

    class Meta:
        db_table = 'Student'

    @staticmethod
    def generate_access_code():
        access_code_list = []
        for student in Student.objects.all():
            firstname = student.firstname
            firstname = firstname[0]
            lastname = student.lastname
            lastname = lastname[0]
            code = student.studentid
            code = code[2:]
            letters_and_digits = string.ascii_letters + string.digits
            result_string = ''.join((random.choice(letters_and_digits) for i in range(6)))
            result_string = firstname + lastname + result_string + code
            access_code_list.append(result_string)
        return access_code_list

class Exampupil(models.Model):
    # examcode = models.TextField(blank=True, null=True)
    # pupilid = models.TextField(blank=True, null=True)
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    examcode_link = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)
    studentid_link = models.ForeignKey(Student,null=True, on_delete=models.CASCADE)
    class Meta:                                                                                                                         
        db_table = 'ExamPupil'


class Classroom(models.Model):                                                          
    roomcode = models.TextField(primary_key=True, blank=True)
    capacity = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Classroom'