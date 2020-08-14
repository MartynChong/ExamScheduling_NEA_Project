from django.shortcuts import render
from django.http import HttpResponse
from .models import Exam

def home(request):
    return HttpResponse('<h1>Database</h1>')

def exams(request):
    allexams = Exam.objects.all()
    context={'allexams': allexams}
    return render(request,'database/exams.html',context)