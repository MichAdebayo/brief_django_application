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

 
    

