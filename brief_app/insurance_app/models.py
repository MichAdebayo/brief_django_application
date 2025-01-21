from django.db import models

class SignUp(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    
class Login(models.Model):
    email = models.ForeignKey(SignUp, null=True, on_delete=models.SET_NULL)
    password = models.ForeignKey(SignUp, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    

    first_name = models.CharField(max_length=200)
    surname_name = models.CharField(max_length=200)
    
    smoker = models.TextChoices("Yes", "No")
    region = models.TextChoices("Northeast", "Northwest", "Southeast", "Southwest")
    sex = models.TextChoices("Male", "Female")

    age = models.IntegerField(max_length=3)
    weight = models.IntegerField(max_length=200)
    height = models.IntegerField(max_length=200) 

    email = models.ForeignKey(SignUp, null=True, on_delete=models.SET_NULL)
    user_name = models.ForeignKey(SignUp, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user_name


