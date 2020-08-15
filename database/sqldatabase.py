import _sqlite3
from .examclass import ExamFile, RoomFile, ExamPupil, NewStudents

conn = _sqlite3.connect("legacy.db")
c = conn.cursor()


ExamInstance = ExamFile()
ExamFile.obtain_data(ExamInstance, 'database\jan21iGCSE.xlsx')

StudentInstance = NewStudents()
NewStudents.create_list(StudentInstance)

RoomInstance = RoomFile()
RoomFile.obtain_data(RoomInstance, 'database\schoolInfo.xlsx')

ExamPupilInstance = ExamPupil()
ExamPupil.create_list(ExamPupilInstance)

class DatabaseInsert:
    conn = _sqlite3.connect("legacy.db")
    c = conn.cursor()

    # Occurs at the beginning
    @classmethod
    def create_db(cls):
        cls.c.execute(""" CREATE TABLE Exam(
        subject text,
        title text,
        code text PRIMARY KEY,
        date text,
        times text,
        duration text
        ) """)
        cls.conn.commit()
        cls.c.execute(""" CREATE TABLE Student(
        studentid text PRIMARY KEY,
        firstname text,
        lastname text,
        birthdate text,
        accessarrangement text
        ) """)
        cls.conn.commit()
        cls.c.execute(""" CREATE TABLE Classroom(
        roomcode text,
        capacity int,
        priority int
        ) """)
        cls.conn.commit()
        cls.c.execute(""" CREATE TABLE ExamPupil(
        examcode text,
        pupilid text,
        ID INTEGER PRIMARY KEY AUTOINCREMENT
        ) """)
        cls.conn.commit()

    @classmethod
    def insert_all_tables(cls):
        cls.create_db()
        cls.mass_insert_exams()
        cls.mass_insert_students()
        cls.mass_insert_exampupil()
        cls.mass_insert_classroom()

    @classmethod
    def mass_insert_exams(cls):
        with cls.conn:
            for i in range(len(ExamInstance.listSubjects)):
                cls.c.execute("INSERT INTO Exam VALUES (:subject,:title,:code,:date,:times,:duration)",
                              {'subject': ExamInstance.listSubjects[i],
                               'title': ExamInstance.listTitle[i],
                               'code': ExamInstance.listCode[i],
                               'date': ExamInstance.listDate[i],
                               'times': ExamInstance.listTimes[i],
                               'duration': ExamInstance.listDuration[i]
                               })
    @classmethod
    def mass_insert_students(cls):
        with cls.conn:
            for i in range(len(StudentInstance.listPupilID)):
                cls.c.execute("INSERT INTO Student VALUES (:studentid,:firstname,:lastname,:birthdate,:accessarrangement)",
                              {'studentid': StudentInstance.listPupilID[i],
                               'firstname': StudentInstance.listFirstname[i],
                               'lastname': StudentInstance.listLastname[i],
                               'birthdate': StudentInstance.listBirthdate[i],
                               'accessarrangement': StudentInstance.listArrangements[i]
                               })

    @classmethod
    def mass_insert_classroom(cls):
        with cls.conn:
            for i in range(len(RoomInstance.listRoomCode)):
                cls.c.execute("INSERT INTO Classroom VALUES (:roomcode,:capacity,:priority)",
                              {'roomcode': RoomInstance.listRoomCode[i],
                               'capacity': RoomInstance.listCapacity[i],
                               'priority': RoomInstance.listPriority[i]
                               })

    @classmethod
    def mass_insert_exampupil(cls):
        with cls.conn:
            for i in range(len(ExamPupilInstance.listExamCode)):
                cls.c.execute("INSERT INTO ExamPupil VALUES (:examcode,:pupilid,:id)",
                              {'examcode': ExamPupilInstance.listExamCode[i],
                               'pupilid': ExamPupilInstance.listPupilID[i],
                               'id': i
                               })

    # @classmethod      
    # def get_exam_by_code(cls, code):
    #     cls.c.execute("SELECT * FROM Exam WHERE code =:code", {'code': code})
    #     return cls.c.fetchone()
    @classmethod
    def get_exam_by_code(cls, code):
        cls.c.execute("SELECT * FROM ExamPupil WHERE examcode =:examcode", {'examcode': code})
        return cls.c.fetchall()


    @classmethod
    def update_exam_time(cls):
        with cls.conn:
            code = cls.input_query()
            print("What time would you like to change to?")
            incorrect = False
            while not incorrect:
                hour = input("What hour would you like to set?")
                minute = input("What minute would you like to set")
                if hour.isdigit() and minute.isdigit():
                    print("Pass1")
                    hour = int(hour)
                    minute = int(minute)
                    if 0 < hour < 24 and minute < 60:
                        time = (str(hour) + ':' + str(minute) + ':' + '00')
                        incorrect = True
                    else:
                        print("Please input a real time")
                else:
                    print("Please input the correct type")
            cls.c.execute("UPDATE MasterExams SET times =:time WHERE code =:code", {'time': time, 'code': code})

    @classmethod
    def input_query(cls):
        with cls.conn:
            code = str(input("Please input a valid Exam code"))
            data = cls.get_exam_by_code(code)
            if not data:
                print("Please input a real value")
                cls.input_query()
            else:
                print(data)
                return code

    # @classmethod
    # def remove_emp(cls, emp):
    #     with cls.conn:
    #         cls.c.execute("DELETE from employees WHERE first = :first AND last = :last",
    #                   {'first': emp.first, 'last': emp.last})


# DatabaseInsert.insert_all_tables()

# # # DatabaseInsert.update_exam_time()
# # # DatabaseInsert.input_query()
# a= DatabaseInsert.get_exam_by_code('4MA1_1F')
# print(a)
