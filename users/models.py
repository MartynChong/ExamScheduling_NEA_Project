from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accesscode = models.TextField(null=True)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

