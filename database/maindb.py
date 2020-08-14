import _sqlite3
from datetime import timedelta
from examclass import Exam 

#Initiates transfer of file 
Exam.obtain_data('database\jan21iGCSE.xlsx')
conn = _sqlite3.connect(":memory:")
c = conn.cursor()

class DatabaseExams:
    conn = _sqlite3.connect(":memory:")
    c = conn.cursor()

    @classmethod
    def create_db(cls):
        cls.c.execute(""" CREATE TABLE MasterExams(
        subject text,
        title text,
        code text,
        date text,
        times text,
        duration text
        ) """)

    @classmethod
    def mass_insert_exam(cls):
        with cls.conn:
            for i in range(0, len(Exam.listSubjects) - 1):
                cls.c.execute("INSERT INTO MasterExams VALUES (:subject,:title,:code,:date,:times,:duration)",
                              {'subject': Exam.listSubjects[i],
                               'title': Exam.listTitle[i],
                               'code': Exam.listCode[i],
                               'date': Exam.listDate[i],
                               'times': Exam.listTimes[i],
                               'duration': Exam.listDuration[i],
                               })


    @classmethod
    def get_exam_by_code(cls, code):
        cls.c.execute("SELECT * FROM MasterExams WHERE code =:code", {'code': code})
        return cls.c.fetchone()

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
                    hour = int(hour)
                    minute = int(minute)
                    if 0 < hour < 24 and minute < 60:
                        time = (str(hour)+':'+str(minute)+':'+'00')
                        incorrect = True
                    else:
                        print("Please input a real time")
                else:
                    print("Please input the correct type")
            cls.c.execute("UPDATE MasterExams SET times =:time WHERE code =:code" ,{'time': time, 'code': code})


    @classmethod
    def input_query(cls):
        with cls.conn:
            # choice = input("Which field would you like to search for?")
            code = str(input("Please input a valid Exam code"))
            print(code)
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


# DatabaseExams.create_db()
# DatabaseExams.mass_insert_exam()
# DatabaseExams.update_exam_time()
# DatabaseExams.input_query()