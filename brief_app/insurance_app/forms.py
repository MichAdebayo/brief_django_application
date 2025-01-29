from django import forms
from .models import UserProfile
from .models import JobApplication  # Assuming you have a JobApplication model to store applications


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password', 'smoker', 'region', 'sex',
                  'age', 'weight', 'height']

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication  # This will be the model for storing application data
        fields = ['name', 'email', 'resume', 'cover_letter']

    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    resume = forms.FileField(required=False)
    cover_letter = forms.CharField(widget=forms.Textarea, required=True)

class InsuranceForm(forms.Form):
    age = forms.IntegerField(label="Age")
    weight = forms.FloatField(label="Weight (in kg)")  # Client's weight
    height = forms.FloatField(label="Height (in meters)")  # Client's height
    children = forms.IntegerField(label="Number of children")
    smoker = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], label="Smoker")
    sex = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], label="Sex")
    region = forms.ChoiceField(choices=[('northeast', 'Northeast'), ('northwest', 'Northwest'), 
                                       ('southeast', 'Southeast'), ('southwest', 'Southwest')], label="Region")