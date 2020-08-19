from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class StudentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accesscode = models.CharField(null=True)


