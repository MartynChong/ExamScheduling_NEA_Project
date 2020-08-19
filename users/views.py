from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import StudentSignUpForm
from .models import User
from django.contrib.auth import login
from django.views.generic import CreateView

# def register(request):
#     if request.method == "POST" :
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username') #Checks the form dictionary for username
#             form.save()
#             messages.success(request, f'Account created for {username}!')
#             return redirect('database-home')
#     else:   
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form':form})


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('database-home')