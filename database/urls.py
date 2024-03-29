from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='database-home'),
    path('exams/', views.exams, name='database-exams'),
    path('search/', views.search, name='database-search'),
    path('search/', views.search, name='database-search'),
    path('rooms/', views.rooms, name='database-rooms'),
    path('exams/<code>/', views.detail_view, name='database-detail'),
    path('clashes/', views.clashes, name='database-clashes'),
    path('myexams/', views.myexams, name='database-myexams'),
    path('studentsearch/', views.studentsearch, name='database-studentsearch'),
    path('studentexams/',views.studentexams, name='database-studentexams')
]