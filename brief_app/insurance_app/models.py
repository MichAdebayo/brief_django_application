from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    class SmokerType(models.TextChoices):
        YES = 'Yes'
        NO = 'No'

    class RegionType(models.TextChoices):
        NORTHEAST = 'Northeast'
        NORTHWEST = 'Northwest'
        SOUTHEAST = 'Southeast'
        SOUTHWEST = 'Southwest'

    class SexType(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'

    age = models.IntegerField(default=False)
    weight = models.IntegerField(default=False)
    height = models.IntegerField(default=False) 
    smoker = models.CharField(blank=True, choices=SmokerType.choices, max_length=10)
    region = models.CharField(blank=True, choices=RegionType.choices, max_length=10)
    sex = models.CharField(blank=True, choices=SexType.choices, max_length=10)

    def __str__(self):
        return self.username

#For the join us job application area
 
class JobApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()

    def __str__(self):
        return self.name
from django.db import models

#To create a list of jobs from the admin page

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100, default="Remote")
    experience = models.CharField(max_length=100, default="Not specified")
    job_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title
    
 #model to store the messages

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    
    