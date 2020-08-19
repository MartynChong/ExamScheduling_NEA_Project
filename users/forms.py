from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from database.models import Student
from django.core.exceptions import ValidationError
from .models import StudentUser
from django.db import transaction


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.Form):
    class Meta:
        model = User
        fields = ['accesscode']
        
    def clean_accesscode(self):
        accesscode = self.cleaned_data['accesscode']
        results = Student.objects.filter(accesscode=accesscode).all()
        if len(results) == 1:
            pass
        else:
            raise ValidationError("Your Access Code does not match any existing codes.")

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField()
    accesscode = ProfileForm()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = StudentUser.objects.create(user=user)
        student.accesscode.add(*self.cleaned_data.get('accesscode'))
        return user