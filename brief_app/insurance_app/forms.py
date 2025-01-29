from django import forms
from .models import UserProfile
from django.contrib.auth.hashers import make_password # Used to hash passwords
from .models import JobApplication  # Assuming you have a JobApplication model to store applications


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username', 'email', 'smoker', 'region', 'sex', 'num_children','age', 'weight', 'height']

class UserSignupForm(forms.ModelForm):                                          # Form based on the UserProfile model
    password = forms.CharField(widget=forms.PasswordInput, label="Password")    # Password field with hidden input

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']                              # Fields displayed in the form

    def save(self, commit=True):
        user = super().save(commit=False)                                       # Create a user object without saving it to the database yet
        user.password = make_password(self.cleaned_data['password'])            # Hash the password before saving
        if commit:
            user.save()                                                         # Save the user to the database
        return user
class UserLoginForm(forms.Form):                                                # Simple form, not based on a model
    username = forms.CharField(max_length=150, label="Username")                # Field for the username
    password = forms.CharField(widget=forms.PasswordInput, label="Password")    # Password field with hidden input

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication  # This will be the model for storing application data
        fields = ['name', 'email', 'resume', 'cover_letter']

    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    resume = forms.FileField(required=False)
    cover_letter = forms.CharField(widget=forms.Textarea, required=True)