from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    smoker = models.BooleanField(default=False)
    region = models.CharField(max_length=10)
    sex = models.BooleanField(default=False)
    age = models.IntegerField(default=False)
    weight = models.IntegerField(default=False)
    height = models.IntegerField(default=False) 

    def __str__(self):
        return self.username
    

