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


# class ExamRoom(models.Model):
#     examcode = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)
#     roomcode = models.ForeignKey(Classroom, null=True, on_delete=models.CASCADE)
#     id = models.AutoField(db_column='ID', primary_key=True)


class ExamRooms():

    def __init__(self):
        self.listExams = []
        self.listRooms = []
        
    @staticmethod
    def count_students_per_exam(examobject):
        studentCount = Exampupil.objects.filter(examcode_link=examobject.code).count()
        return studentCount
    
    def same_session():
        continue_adding = True
        exam_instance = list(Exam.objects.all())
        sessions = []
        counter = -1
        broken = False
        while not broken:
            try:
                counter += 1
                codedict = {
                    "session": counter,
                    "exam": []
                }
                same_time = Exam.objects.filter(times=exam_instance[0].times, date = exam_instance[0].date)
                for i in range(len(same_time)):
                    exam_instance.remove(same_time[i])
                codedict['exam'].append(((same_time)))
                sessions.append(codedict)
            except:
                broken = True
        return sessions
            
            

    def determine_exam_pairings(self):
        sessions = ExamRooms.same_session()
        count = -1
        for i in range (len(sessions)):
            sessionlength = len(sessions[i]['exam'][0])
            classstack = ClassroomStack()
            ClassroomStack.generate_instance(classstack)
            for k in range((sessionlength)):
                self.listExams.append(sessions[i]['exam'][0][k])
                currentcount = ExamRooms.count_students_per_exam(sessions[i]['exam'][0][k])
                size_fit = False
                count = 0
                while size_fit == False:
                    print('Exam',sessions[i]['exam'][0][k], 'Room',classstack.rooms[len(classstack.rooms)-(count+1)],'Currentcount',currentcount,'Room stack',classstack.capacity[len(classstack.capacity)-(count+1)])
                    if currentcount <= classstack.capacity[len(classstack.capacity)-(count+1)]:
                        currentroom = classstack.rooms[len(classstack.rooms)-(count+1)]
                        print('Current Room Taken',currentroom)
                        self.listRooms.append(currentroom)
                        size_fit = True
                        classstack.pop()
                    else:
                        print("Room Fail",sessions[i]['exam'][0][k],classstack.rooms[len(classstack.rooms)-(count+1)])
                        count += 1

        



class ClassroomStack():

    def __init__(self):
        self.rooms = []
        self.capacity = []
        self.priority = []

    def flip_lists(self):
        self.rooms=self.rooms[::-1]
        self.capacity=self.capacity[::-1]
        self.priority=self.priority[::-1]
    
    def generate_instance(self):
        for i in Classroom.objects.all():
            self.rooms.append(i.roomcode)
            self.capacity.append(i.capacity)
            self.priority.append(i.priority)
        self.flip_lists()

    def push(self, data):
        self.rooms.append(data)
    
    def pop(self):
        self.rooms.pop()
        self.capacity.pop()
        self.priority.pop()
        





# import sys
    # def sort_object_order(self, listpriority):
    #     for i in range(0, len(self.rooms)-1):
    #         priorityroom = self.rooms[(listpriority[i])]
    #         prioritycapacity = self.capacity[(listpriority[i])]
    #         if self.priority[i] > listpriority[i]:
    #             temproom = self.rooms[i]
    #             tempcapacity = self.rooms[i]
    #             self.rooms[i] = priorityroom
    #             self.rooms[i] = prioritycapacity
    #             self.rooms[(listpriority[i])]= temproom
    #             self.capacity[(listpriority[i])]= tempcapacity

#     def merge_sort_priority(listpriority):
#         merge_sort2(listpriority, 0, len(listpriority) - 1)

#     #first, middle, last index
#     def merge_sort_priority_recursive(listpriority, first, last):
#         if first < last:
#             middle = (first + last) // 2
#             merge_sort_priority_recursive(A, first, middle)
#             merge_sort_priority_recursive(A, middle + 1, last)
#             merge(A, first, middle, last)
#             print(A)

#     def merge_lists(listpriority, first, middle, last):
#         Left = listpriority[first:middle + 1]
#         Right = listpriority[middle + 1:last + 1]
#         Left.append(sys.maxsize)
#         Right.append(sys.maxsize)
#         i = j = 0

#         for k in range(first, last + 1):
#             if Left[i] <= Right[j]:
#                 listpriority[k] = Left[i]
#                 i += 1
#             else:
#                 Left[k] = Right[j]
#                 j += 1

# classtest = ClassroomStack()
# ClassroomStack.generate_instance(classtest)
# print(classtest.rooms)
# print(classtest.capacity)