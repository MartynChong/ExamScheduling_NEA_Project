from django.shortcuts import render
from django.http import HttpResponse
from .models import Exam


def home(request):
    allexams = Exam.objects.all()
    context={'allexams': allexams}
    return render(request,'database/home.html',context, )

def exams(request):
    allexams = Exam.objects.all()
    context={'allexams': allexams}
    return render(request,'database/exams.html',context)

# def search(request):
#     template = 'database/exams.html'