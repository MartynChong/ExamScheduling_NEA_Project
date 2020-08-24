from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Exam, ExamRooms, Clashes, Exampupil, Student
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Account



def home(request):
    return render(request,'database/home.html')


def exams(request):
    allexams = Exam.objects.all().order_by('date')
    context={'allexams': allexams}
    return render(request,'database/exams.html',context)

def search(request):
    template = 'database/exams.html'
    query = request.GET.get('q')
    results = Exam.objects.filter(Q(title__icontains=query) | Q(code__icontains=query) | Q(subject__icontains=query) | Q(times__icontains=query) | Q(date__icontains=query) | Q(duration__icontains=query))
    context= {'allexams':results}
    return render(request, template, context)


def rooms(request):
    examrooms = ExamRooms()
    ExamRooms.determine_exam_pairings(examrooms)
    zipped = zip(examrooms.listExams,examrooms.listRooms)
    context={'listexamsandrooms': zipped
        }
    return render(request, 'database/rooms.html',context)


def detail_view(request, code):
    pupils = Exampupil.objects.filter(examcode_link= Exam.objects.get(code = code)).all()
    pupillist=[]
    for i in range(len(pupils)):
        pupil = Student.objects.filter(studentid=pupils[i].studentid_link.studentid).first()
        pupillist.append(pupil)
    context = {
        'data': Exam.objects.get(code = code),
        'pupils': pupillist
    }
    
    return render(request, 'database/detail_view.html',context)


@login_required
def clashes(request):
    if request.user.is_superuser == True:
        clashInstance = Clashes()
        Clashes.displaying_clash(clashInstance)
        zipped = Clashes.generate_zip_view(clashInstance)
        currentexams=[]
        if request.method == 'POST':
            #Finding which clash exams were chosen to be updated
            for i in range(len(clashInstance.listIndividualExams)):
                if request.POST.get((clashInstance.listIndividualExams[i].code)):
                    currentexams.append(clashInstance.listIndividualExams[i])
                    currentexams.append(clashInstance.listIndividualExams[i+1])
            Clashes.update_other_tables(clashInstance, currentexams)
            messages.success(request, f'Clash was resolved!')
            return redirect('database-home')
    else:
        messages.warning(request, f'Only Admins can enter the clash site')
        return redirect('database-home')
            
    context={'listClashes': zipped}
    return render(request, 'database/clashes.html',context)

@login_required
def myexams(request):
    currentuser = Account.objects.filter(user = request.user).first()
    if currentuser.is_teacher == False and currentuser.is_admin == False:
        currentstudent = Student.objects.filter(accesscode = currentuser.accesscode).first()
        allmyexams = Exampupil.objects.filter(studentid_link= currentstudent).all()
        currentexams = []
        for i in range (len(allmyexams)):
            allexams = Exam.objects.filter(code=allmyexams[i].examcode_link.code).first()
            currentexams.append(allexams)
        context={'allexams': currentexams}
    else:
        return redirect('database-studentsearch')
    return render(request,'database/myexams.html',context)


@login_required
def studentsearch(request):
    currentuser = Account.objects.filter(user = request.user).first()
    if currentuser.is_teacher == True or currentuser.is_admin == True:
        pass
    else:
        messages.warning(request, f'You can only view your own exams')
        return redirect('database-myexams')
    return render(request, 'database/studentsearch.html')


@login_required
def studentexams(request):
    currentuser = Account.objects.filter(user = request.user).first()
    if currentuser.is_teacher == True or currentuser.is_admin == True:
        query = request.GET.get('q')
        currentstudent = Student.objects.filter(studentid = query).first()
        if currentstudent:
            allmyexams = Exampupil.objects.filter(studentid_link= currentstudent).all()
            currentexams = []
            for i in range (len(allmyexams)):
                allexams = Exam.objects.filter(code=allmyexams[i].examcode_link.code).first()
                currentexams.append(allexams)
            context={'allexams': currentexams,
                     'student': currentstudent}
        else:
            messages.warning(request, f'No student with that code was found')
            return redirect('database-studentsearch')
    else:
        return redirect('database-myexams')
    return render(request, 'database/studentexams.html', context)


