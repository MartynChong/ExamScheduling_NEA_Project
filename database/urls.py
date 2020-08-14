from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='database-home'),
    path('/exams', views.exams, name='database-exams'),
]