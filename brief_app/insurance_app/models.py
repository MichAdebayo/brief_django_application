from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    surname_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=200)
    smoker = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    weight = models.CharField(max_length=200)
    height = models.CharField(max_length=200) 
    sex = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name
    
class Login_and_SignUp(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class SignUp(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    

