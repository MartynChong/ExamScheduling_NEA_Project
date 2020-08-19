from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from database.models import Student
from django.core.exceptions import ValidationError
from .models import Account

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    accesscode = forms.CharField(label='Enter Access Code',min_length=4, max_length=20 )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def clean_accesscode(self):
        accesscode = self.cleaned_data['accesscode']
        results = Student.objects.filter(accesscode=accesscode).all()
        if len(results) == 1 or accesscode == 'cLqbug53Vi' or accesscode == 'fvLbfNYUTw':
            pass
        else:
            raise ValidationError("Your Access Code does not match any existing codes.")
        
        return accesscode

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        if self.cleaned_data['accesscode'] == 'cLqbug53Vi':
            account = Account.objects.create(user= user,accesscode= self.cleaned_data['accesscode'], is_admin= True)
        elif self.cleaned_data['accesscode'] == 'fvLbfNYUTw':
            account = Account.objects.create(user= user,accesscode= self.cleaned_data['accesscode'], is_teacher= True)
        else:
            account = Account.objects.create(user= user,accesscode= self.cleaned_data['accesscode'])
        return user


# class ProfileForm(forms.Form):
#     class Meta:
#         model = StudentUser
#         fields = ['accesscode']
        
#     def clean_accesscode(self):
#         accesscode = self.cleaned_data['accesscode']
#         results = Student.objects.filter(accesscode=accesscode).all()
#         if len(results) == 1:
#             pass
#         else:
#             raise ValidationError("Your Access Code does not match any existing codes.")

        

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#     accesscode = ProfileForm()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


