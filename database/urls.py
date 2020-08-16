from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='database-home'),
    path('exams/', views.exams, name='database-exams'),
    path('search/', views.search, name='database-search'),
    path('rooms/', views.rooms, name='database-rooms'),
    path('roomsearch/', views.rooms, name='database-roomsearch'),
]