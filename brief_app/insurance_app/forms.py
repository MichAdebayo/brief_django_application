from django import forms
from .models import UserProfile
from django.contrib.auth.hashers import make_password # Used to hash passwords

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password', 'smoker', 'region', 'sex',
                  'age', 'weight', 'height']

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

'''This form is not a ModelForm because it doesn't modify or create data in the database. It only validates the user's input.'''
