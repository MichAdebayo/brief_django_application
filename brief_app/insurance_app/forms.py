from django import forms
from .models import UserProfile
from .models import JobApplication  # Assuming you have a JobApplication model to store applications


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password', 'smoker', 'region', 'sex', 'num_children',
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