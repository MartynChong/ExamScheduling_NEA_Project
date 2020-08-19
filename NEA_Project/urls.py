from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('database.urls')),
    path('register/', user_views.register, name='register'),
    path('register/student', user_views.StudentSignUpView.as_view(), name='student-signup')
]
