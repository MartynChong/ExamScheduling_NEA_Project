from django.db import models
import random, string
from datetime import timedelta, datetime

class Exam(models.Model):
    subject = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    code = models.TextField(primary_key=True, blank=True)
    date = models.TextField(blank=True, null=True)
    times = models.TextField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)
    clash_done = models.BooleanField(null=True, default=False)

    class Meta:
        db_table = 'Exam'
    
        

class Student(models.Model):
    studentid = models.TextField(primary_key=True, blank=True)
    firstname = models.TextField(blank=True, null=True)
    lastname = models.TextField(blank=True, null=True)
    birthdate = models.TextField(blank=True, null=True)
    accessarrangement = models.TextField(blank=True, null=True)
    accesscode = models.TextField(null = True)
    accountmade = models.BooleanField(null=True, default=False)

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

        #This while loop takes all Exams, filtered by date, and sorted by duration, to create a dictionary of Sessions and the exams within
        while not broken:
            try:
                removelist = []
                counter += 1
                codedict = {
                    "session": counter,
                    "exam": []
                }
                same_time = Exam.objects.filter(date = exam_instance[0].date)
                
    
                if len(same_time) != 1:
                    for i in range(len(same_time)):
                        basetime = datetime.strptime(exam_instance[0].times, '%H:%M:%S')
                        duration = timedelta(hours=2)
                        newtime = datetime.strptime(same_time[i].times, '%H:%M:%S')
                        #If the difference in start times are < 4 hours, they are considered the same session
                        #If the difference is > 4 hours, they are added to the removelist to be removed from the same session
                        if not -duration < (newtime-basetime) < duration:
                            removelist.append(same_time[i].code)
                
                    #Removing removelist from same session
                    for k in range(len(removelist)):
                        a = removelist[k]
                        try:
                            same_time = same_time.exclude(code=a)
                        except:
                            pass
                    codedict['exam'].append(((same_time)))

                    #Removing same session exams from the base Exam list
                    for i in range(len(same_time)):
                        try:
                            exam_instance.remove(same_time[i])
                        except:
                            pass
                else:
                    #Appends the code dictionary with the session instance
                    codedict['exam'].append(((same_time)))
                    exam_instance.remove(same_time[0])


                sessions.append(codedict)
            except:
                broken = True
        return sessions
            
            

    def determine_exam_pairings(self):
        sessions = ExamRooms.same_session()
        count = -1

        #Loops for the number of sessions
        for i in range (len(sessions)):
            sessionlength = len(sessions[i]['exam'][0])
            classstack = ClassroomStack()
            ClassroomStack.generate_instance(classstack)

            #Loops for the length of each session
            for k in range((sessionlength)):
                self.listExams.append(sessions[i]['exam'][0][k])
                #Counts up the number of students in this session's exam
                currentcount = ExamRooms.count_students_per_exam(sessions[i]['exam'][0][k])
                size_fit = False
                count = 0

                
                #While the size of the room cannot fit the student count, skip to the next room
                #If the size fits, pop the room off the stack for this session
                while size_fit == False:
                    if currentcount <= classstack.capacity[len(classstack.capacity)-(count+1)]:
                        currentroom = classstack.rooms[len(classstack.rooms)-(count+1)]

                        self.listRooms.append(currentroom)
                        size_fit = True
                        classstack.pop((len(classstack.rooms)-(count+1)))
                    else:
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
    
    #Generates Classroom instance
    def generate_instance(self):
        for i in Classroom.objects.all():
            self.rooms.append(i.roomcode)
            self.capacity.append(i.capacity)
            self.priority.append(i.priority)
        self.flip_lists()

    def push(self, data):
        self.rooms.append(data)
    
    def pop(self, index):
        self.rooms.pop(index)
        self.capacity.pop(index)
        self.priority.pop(index)


class Clashes():

    def __init__(self):
        #Variables used to identify Clash
        self.listStudentsInClash = []
        self.listExamsInClash = []
        #Variables used to declare Clashes
        self.listCurrentExams = []
        self.listNewIndividualExams = []
        self.listIndividualExams = []
        self.listCurrentStudents = []
        self.listOldStartTime = []
        self.listNewStartTime = []
        self.listDuration = []
        self.listOldEndTime = []
        self.listNewEndTime = []
        self.listDate = []
        self.listExtraTime = []
        #Variable used to update student values
        self.listDuplicateStudentsInClash = []
        


    #This function alters the init lists to include sets of clashing exams and the students involved
    def identify_students_clash(self):
        sessions = ExamRooms.same_session()
        sessions = [n for n in sessions if not True in n.clash_done]
        for currentSession in range(len(sessions)):
            sessionlength = len(sessions[currentSession]['exam'][0])
            if sessionlength > 1:

                #For loop runs through the number of exams in the session
                for examInSession in range(sessionlength-1):

                    #Initialises the current target exam and the students who take it
                    studentsInExam = Exampupil.objects.filter(examcode_link=sessions[currentSession]['exam'][0][examInSession])
                    setStudents = set()
                    nextexam = 1
                    for k in range(len(studentsInExam)):
                        setStudents.add(studentsInExam[k].studentid_link)
                    # print('Current Exam',sessions[currentSession]['exam'][0][examInSession], 'Students Within',setStudents)

                    #This loop initialises the next exams in the session and their students and obtains the intersecting students
                    while nextexam < sessionlength:
                        studentsInNextExam = Exampupil.objects.filter(examcode_link=sessions[currentSession]['exam'][0][nextexam])
                        setStudentsNextExam = set()
                        currentExamsCompare = {sessions[currentSession]['exam'][0][examInSession],sessions[currentSession]['exam'][0][nextexam]}
                        for k in range(len(studentsInNextExam)):
                            setStudentsNextExam.add(studentsInNextExam[k].studentid_link)
                        # print("Current Competing Exam", sessions[currentSession]['exam'][0][nextexam], 'Students Within', setStudentsNextExam)
                        if len(currentExamsCompare) != 1:
                            # print("Current Clashing Exams", currentExamsCompare)
                            if setStudents.intersection(setStudentsNextExam):
                                # print("Clash of Exams", currentExamsCompare, "Students:", setStudents.intersection(setStudentsNextExam))
                                self.listStudentsInClash.append(setStudents.intersection(setStudentsNextExam))
                                self.listDuplicateStudentsInClash.append(setStudents.intersection(setStudentsNextExam))
                                self.listDuplicateStudentsInClash.append(setStudents.intersection(setStudentsNextExam))
                                self.listExamsInClash.append(currentExamsCompare)
                                nextexam += 1
                            else:
                                nextexam += 1
                        else:
                            nextexam += 1

    def displaying_clash(self):
        self.identify_students_clash()
        index = 0

        #Iterate through all clashing exams
        for currentclash in range (len(self.listExamsInClash)):

            #Generating String List of the 2 Clashing Exams
            temp = []
            for i in self.listExamsInClash[currentclash]:
                temp.append(i)
                self.listIndividualExams.append((i))
                newName = i.code + "__2"
                self.listNewIndividualExams.append(newName)
            currentexams = str(temp[0].code) + ', ' + str(temp[1].code)
            self.listCurrentExams.append(currentexams)
            self.listCurrentExams.append(currentexams)
            #Generating String List of the students clashing in those two exams
            temp = []
            for i in self.listStudentsInClash[currentclash]:
                temp.append(i)
            currentstudents = ''
            count = 0
            for i in range (len(temp)):
                if count == (len(temp)-1):
                    currentstudents = currentstudents + str(temp[i].studentid)
                    count += 1
                else:
                    currentstudents = currentstudents + str(temp[i].studentid) + ','
                    count += 1
            self.listCurrentStudents.append(currentstudents)
            self.listCurrentStudents.append(currentstudents)

            #Generating String List of the OLD duration, times of each clashing exam
            for i in self.listExamsInClash[currentclash]:
                self.listOldStartTime.append(i.times)
                duration = Clashes.convert_duration(i.duration)
                self.listDuration.append(duration)
                self.listDate.append(i.date)
                self.listExtraTime.append(False)
                #Generating String List of the OLD end times, generated from the start times and duration
                temp = []
                #Checking if students involved have Extra Time requirements
                for r in self.listStudentsInClash[currentclash]:
                    temp.append(r)
                extra_time = False
                for k in range(len(temp)):
                    if temp[k].accessarrangement == 'Extra Time (25%)':
                        extra_time = True
                if extra_time == True:
                    self.listDuration[index] = self.listDuration[index] * 1.25
                    self.listExtraTime[index] = True
                starttime = datetime.strptime(i.times, '%H:%M:%S')
                endtime = (starttime + self.listDuration[index]).time()
                endtime = str(endtime)
                self.listOldEndTime.append(endtime)
                index = index + 1

            #Generating String List of NEW start/end times
        for exam1 in range(0, len(self.listOldStartTime),2):
            #Making the earlier exam start 30 mins earlier and finding the end time
            timechange = timedelta(minutes=30)
            currenttime = datetime.strptime(str(self.listOldStartTime[exam1]), '%H:%M:%S')
            currenttime = currenttime - timechange
            endtime = (currenttime + self.listDuration[exam1])
            self.listNewEndTime.append(str(endtime.time()))
            currenttime = str(currenttime.time())
            self.listNewStartTime.append(currenttime)

            #Making the start/end times for the later consecutive exam
            starttime2 = timedelta(minutes=15) + endtime
            endtime2 = starttime2 + self.listDuration[exam1+1]
            self.listNewEndTime.append(str(endtime2.time()))
            self.listNewStartTime.append(str(starttime2.time()))
    
                          
    @staticmethod
    def convert_duration(selectedDur):
        currentDur = selectedDur
        hour = int(currentDur[0:1])
        minutes = int(currentDur[3:5])
        selectedDur = timedelta(hours=hour, minutes=minutes)
        return selectedDur

    def convert_duration_back(self):
        for i in range(len(self.listDuration)):
            duration = self.listDuration[i]
            stringduration = str(duration)
            list = stringduration.split(':')
            newvalue = list[0] + 'h ' + list[1] + 'm'
            self.listDuration[i] = newvalue
    
    #Generates the zip view used to display in html
    def generate_zip_view(self):
        zipped = []
        for i in range(0, len(self.listIndividualExams), 2):
            zipped.append((
                self.listCurrentExams[i],
                self.listCurrentStudents[i],
                self.listExtraTime[i],
                self.listIndividualExams[i].code,
                self.listIndividualExams[i + 1].code,
                self.listDate[i],
                self.listOldStartTime[i],
                self.listOldStartTime[i + 1],
                self.listOldEndTime[i],
                self.listOldEndTime[i + 1],
                self.listNewIndividualExams[i],
                self.listNewIndividualExams[i + 1],
                self.listNewStartTime[i],
                self.listNewStartTime[i + 1],
                self.listDuration[i],
                self.listDuration[i + 1],
                self.listNewEndTime[i],
                self.listNewEndTime[i + 1],
            ))
        return zipped

    
    def update_other_tables(self, examschosen):
        self.convert_duration_back()

        for i in range(len(examschosen)):
            #Updating Exam Objects with new Instances
            for k in range(len(self.listIndividualExams)):
                 if examschosen[i] == self.listIndividualExams[k]:  
                    index = k
            #Creates a new Exam object with the new Clash Values
            code = self.listNewIndividualExams[index]
            date = self.listIndividualExams[index].date
            duration = self.listDuration[index]
            subject = self.listIndividualExams[index].subject
            title = self.listIndividualExams[index].title
            time = self.listNewStartTime[index]
            e = Exam.objects.create(subject=subject,title=title,code=code,date=date,times=time,duration=duration, clash_done=True)

            #Updating Students taking those exams
            studentsinvolved = self.listDuplicateStudentsInClash[index]
            for k in range(len(studentsinvolved)):
                currentstudent = studentsinvolved.pop()
                searchstudents = Exampupil.objects.filter(studentid_link=currentstudent,examcode_link=self.listIndividualExams[index])
                updatestudent = searchstudents[0]
                print(updatestudent)
                updatestudent.examcode_link = e
                updatestudent.save()
                print(updatestudent.examcode_link, code)

        



        


    # def print_all(self):
    #     print(self.listCurrentExams ,
    #     self.listCurrentStudents ,
    #     self.listOldStartTime ,
    #     self.listNewStartTime ,
    #     self.listDuration ,
    #     self.listOldEndTime ,
    #     self.listNewEndTime ,
    #     self.listDate )
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


