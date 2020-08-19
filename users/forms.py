from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from database.models import Student
from django.core.exceptions import ValidationError
from .models import StudentUser
from django.db import transaction


class ProfileForm(forms.Form):
    class Meta:
        model = StudentUser
        fields = ['accesscode']
        
    def clean_accesscode(self):
        accesscode = self.cleaned_data['accesscode']
        results = Student.objects.filter(accesscode=accesscode).all()
        if len(results) == 1:
            pass
        else:
            raise ValidationError("Your Access Code does not match any existing codes.")

        

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    accesscode = ProfileForm()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


