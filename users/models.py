from django.db import models
from django.contrib.auth.models import User

class StudentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accesscode = models.TextField(null=True)


