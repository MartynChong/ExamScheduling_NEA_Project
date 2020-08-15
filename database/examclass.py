import xlrd
import datetime
from datetime import timedelta
import re
# from models import ExamPupil


class File:
    # Opening standardised Edexcel timetable xlsx file
    @staticmethod
    def open_file(filename, filetype):
        wb = xlrd.open_workbook(filename)
        if filetype == 'exams':
            search = 'All papers'
        elif filetype == 'students':
            search = 'Students'
        elif filetype == 'rooms':
            search = 'Rooms'
        page = (wb.sheet_by_name(search))
        return page

    # Converting between Excel date to Python Date format
    @staticmethod
    def convert_xldate_to_datetime(xldate):
        try:
            temp = datetime.datetime(1899, 12, 30)
            delta = datetime.timedelta(days=xldate)
            newdate = str(temp + delta)
        except:
            newdate = xldate
        return newdate


class ExamFile(File):
    # Initiating variables
    def __init__(self):
        self.listSubjects = []
        self.listTitle = []
        self.listTimes = []
        self.listCode = []
        self.listDate = []
        self.listDuration = []

    # Converting the Duration string into a datetime value
    @staticmethod
    def convert_duration(selectedDur):
        currentDur = selectedDur
        hour = int(currentDur[0:1])
        minutes = int(currentDur[3:5])
        selectedDur = timedelta(hours=hour, minutes=minutes)
        return selectedDur
    
    def convert_datetime_to_date(self):
        timelist = self.listTimes
        for i in range(len(timelist)):
            newtime =  timelist[i]
            newtime = newtime[0:10]   
            timelist[i] = newtime
        return timelist

    # Obtaining the exam data from the xlsx file and inserting them into arrays
    def obtain_data(self, filename):
        page = ExamFile.open_file(filename, 'exams')
        count = 0
        broken = False
        while not broken:
            count = count + 1
            try:
                selectedDate = self.convert_xldate_to_datetime(page.cell(count, 0).value)
                selectedCode = page.cell(count, 4).value
                selectedSub = page.cell(count, 5).value
                selectedTitle = page.cell(count, 6).value
                selectedTime = page.cell(count, 7).value
                selectedDur = page.cell(count, 8).value
                self.listDate.append(selectedDate)
                if selectedTime == 'Morning':
                    selectedTime = str(timedelta(hours=9))
                elif selectedTime == 'Afternoon':
                    selectedTime = str(timedelta(hours=13, minutes=30))
                self.listTimes.append(selectedTime)
                self.listSubjects.append(selectedSub)
                self.listTitle.append(selectedTitle)
                self.listCode.append(selectedCode)
                self.listDuration.append(selectedDur)
            except:
                broken = True


class StudentFile(File):

    def __init__(self):
        self.listID = []
        self.listFirstname = []
        self.listLastname = []
        self.listExamtaking = []
        self.listBirthdate = []
        self.listArrangements = []

    def obtain_data(self, filename):
        page = ExamFile.open_file(filename, 'students')
        count = 0
        broken = False
        while not broken:
            count = count+1
            try:
                selectedID = page.cell(count, 0).value
                selectedFirstname = page.cell(count, 1).value
                selectedLastname = page.cell(count, 2).value
                selectedExamtaking = page.cell(count, 3).value
                selectedBirthdate = self.convert_xldate_to_datetime(page.cell(count, 4).value)
                selectedArrangements = page.cell(count, 5).value
                self.listID.append(selectedID)
                self.listFirstname.append(selectedFirstname)
                self.listLastname.append(selectedLastname)
                self.listExamtaking.append(selectedExamtaking)
                self.listBirthdate.append(selectedBirthdate)
                self.listArrangements.append(selectedArrangements)
            except:
                broken = True


class RoomFile(File):

    def __init__(self):
        self.listRoomCode = []
        self.listPriority = []
        self.listCapacity = []

    def obtain_data(self, filename):
        page = ExamFile.open_file(filename, 'rooms')
        count = 0
        broken = False
        while not broken:
            count = count+1
            try:
                selectedRoomCode = page.cell(count, 0).value
                selectedCapacity = page.cell(count, 1).value
                selectedPriority = page.cell(count, 2).value
                self.listRoomCode.append(selectedRoomCode)
                self.listPriority.append(int(selectedPriority))
                self.listCapacity.append(int(selectedCapacity))
            except:
                broken = True

class SortDatabase:

    @staticmethod
    def obtain_files(choice):
        if choice == 'Exams':
            ExamInstance = ExamFile()
            ExamFile.obtain_data(ExamInstance, 'database\jan21iGCSE.xlsx')
            return ExamInstance
        elif choice == 'Students':
            StudentInstance = StudentFile()
            StudentFile.obtain_data(StudentInstance, 'database\schoolInfo.xlsx')
            return StudentInstance
        elif choice == 'Rooms':
            RoomInstance = RoomFile()
            RoomFile.obtain_data(RoomInstance, 'database\schoolInfo.xlsx')
            return RoomInstance


class ExamPupil(SortDatabase):
    def __init__(self):
        self.listExamCode = []
        self.listPupilID = []

    def obtain_matching_values(self):
        ExamInstance = self.obtain_files('Exams')
        StudentInstance = self.obtain_files('Students')
        examList = []
        for examNo in range(len(ExamInstance.listCode)):
            codedict = {
                "key": ExamInstance.listCode[examNo],
                "pupil": []
            }
            for pupilNo in range(len(StudentInstance.listExamtaking)):
                if ExamInstance.listCode[examNo] == StudentInstance.listExamtaking[pupilNo]:
                    value = StudentInstance.listID[pupilNo]
                    codedict['pupil'].append(value)
            examList.append(codedict)
        return examList

    def create_list(self):
        examList = self.obtain_matching_values()
        for keyNo in range(len(examList)):
            listExams = examList[keyNo]
            for studentNo in range(len(listExams['pupil'])):
                key = listExams['key']
                pupil = listExams['pupil'][studentNo]
                self.listExamCode.append(key)
                self.listPupilID.append(pupil)


class NewStudents(SortDatabase):
    def __init__(self):
        self.listPupilID = []
        self.listFirstname = []
        self.listLastname = []
        self.listBirthdate = []
        self.listArrangements = []

    def create_list(self):
        StudentInstance = self.obtain_files('Students')
        listID = []
        listAppeared = []
        for i in range(len(StudentInstance.listID)):
            if not StudentInstance.listID[i] in listAppeared:
                listAppeared.append(StudentInstance.listID[i])
                name_Appeared = {StudentInstance.listID[i], i}
                listID.append(name_Appeared)
        for i in range(len(listID)):
            popItem = str(listID[i].pop())
            pattern = '(MY)(\d\d\d)'
            result = re.match(pattern, popItem)
            if result:
                popIndex = listID[i].pop()
                self.listPupilID.append(StudentInstance.listID[popIndex])
                self.listFirstname.append(StudentInstance.listFirstname[popIndex])
                self.listLastname.append(StudentInstance.listLastname[popIndex])
                self.listBirthdate.append(StudentInstance.listBirthdate[popIndex])
                self.listArrangements.append(StudentInstance.listArrangements[popIndex])
            else:
                popItem = int(popItem)
                self.listPupilID.append(StudentInstance.listID[popItem])
                self.listFirstname.append(StudentInstance.listFirstname[popItem])
                self.listLastname.append(StudentInstance.listLastname[popItem])
                self.listBirthdate.append(StudentInstance.listBirthdate[popItem])
                self.listArrangements.append(StudentInstance.listArrangements[popItem])

print("hi")