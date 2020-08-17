from django.shortcuts import render
from django.http import HttpResponse
from .models import Exam, ExamRooms
from django.db.models import Q



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
    print(results)
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
    context = {
    }
    context["data"] = Exam.objects.get(code = code)
    return render(request, 'database/detail_view.html',context)