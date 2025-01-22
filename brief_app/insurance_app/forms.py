from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password', 'smoker', 'region', 'sex',
                  'age', 'weight', 'height']
