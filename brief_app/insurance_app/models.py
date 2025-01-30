from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    class SmokerType(models.TextChoices):
        YES = 'Yes', 'Yes'
        NO = 'No', 'No'

    class RegionType(models.TextChoices):
        NORTHEAST = 'Northeast', 'Northeast'
        NORTHWEST = 'Northwest', 'Northwest'
        SOUTHEAST = 'Southeast', 'Southeast'
        SOUTHWEST = 'Southwest', 'Southwest'

    class SexType(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    # Personal Info
    age = models.PositiveIntegerField(default=25)
    weight = models.PositiveIntegerField(default=60, help_text="Weight in kilograms")
    height = models.PositiveIntegerField(default=170, help_text="Height in centimeters")
    num_children = models.PositiveIntegerField(default=0)
    
    # Choice-based Fields
    smoker = models.CharField(
        blank=False,
        max_length=10,
        choices=SmokerType.choices
    )
    region = models.CharField(
        blank=False,
        max_length=10,
        choices=RegionType.choices,
    )
    sex = models.CharField(
        blank=False,
        max_length=10,
        choices=SexType.choices,
    )

    # Calculated Property
    @property
    def bmi(self):
        """Calculate BMI safely with zero division protection"""
        if self.height <= 0:
            return 0.0
        return round(self.weight / ((self.height / 100) ** 2), 1)

    def __str__(self):
        return f"{self.username}"

class PredictionHistory(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='insurance_predictions'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Frozen User State
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    num_children = models.PositiveIntegerField()
    smoker = models.CharField(max_length=10)
    region = models.CharField(max_length=10)
    sex = models.CharField(max_length=10)
    
    # Prediction Result
    predicted_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Predicted insurance charges in USD"
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Insurance Prediction"
        verbose_name_plural = "Insurance Predictions"
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]

    # Derived Field
    @property
    def bmi(self):
        """Preserve historical BMI calculation"""
        if self.height <= 0:
            return 0.0
        return round(self.weight / ((self.height / 100) ** 2), 1)

    def __str__(self):
        return f"{self.user} prediction @ {self.timestamp:%Y-%m-%d}"
    

# For the join us job application area
class JobApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()

    def __str__(self):
        return self.name
    

# To create a list of jobs from the admin page
class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100, default="Remote")
    experience = models.CharField(max_length=100, default="Not specified")
    job_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title


 # Model to store the messages
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    




