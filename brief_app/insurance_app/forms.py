from django import forms
from .models import UserProfile
from .models import JobApplication, Appointment
from django.utils.html import format_html
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
#from django_flatpickr.widgets import DatePickerInput  # or another widget type
from .models import Appointment


class PredictChargesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["age", "height", "weight", "num_children", "smoker"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "smoker",
            "region",
            "sex",
            "num_children",
            "age",
            "weight",
            "height",
        ]


class UserSignupForm(forms.ModelForm):  # Form based on the UserProfile model
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password"
    )  # Password field with hidden input

    class Meta:
        model = UserProfile
        fields = ["username", "email", "password"]  # Fields displayed in the form

    def save(self, commit=True):
        user = super().save(
            commit=False
        )  # Create a user object without saving it to the database yet
        user.password = make_password(
            self.cleaned_data["password"]
        )  # Hash the password before saving
        if commit:
            user.save()  # Save the user to the database
        return user


class UserLoginForm(forms.Form):  # Simple form, not based on a model
    username = forms.CharField(
        max_length=150, label="Username"
    )  # Field for the username
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password"
    )  # Password field with hidden input


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication  # This will be the model for storing application data
        fields = ["name", "email", "resume", "cover_letter"]

    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    resume = forms.FileField(required=False)
    cover_letter = forms.CharField(widget=forms.Textarea, required=True)


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize labels
        self.fields["old_password"].label = "Current Password"
        self.fields["new_password1"].label = "New Password"
        self.fields["new_password2"].label = "Confirm New Password"

        # Add help text for password requirements
        self.fields["new_password1"].help_text = format_html(
            '<ul class="text-sm text-gray-600 mt-2">'
            "<li>Your password must be at least 8 characters long.</li>"
            "<li>Your password cannot be entirely numeric.</li>"
            "<li>Your password cannot be too similar to your other personal information.</li>"
            "</ul>"
        )

        # Add Tailwind CSS classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-400",
                }
            )


## Appoinment form

from django.forms import DateInput

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['reason', 'date', 'time']
        widgets = {
            'date': DateInput(attrs={'type': 'date', 'class': 'form-control w-full bg-gray-100 rounded-md p-2'}),
        }

    # Optionally, you can add validation for the time field
    def clean_time(self):
        time = self.cleaned_data.get('time')
        # Example validation: Make sure time follows HH:MM format (24-hour clock)
        try:
            if not time:  # Check if time is empty
                raise forms.ValidationError("This field is required.")
            hour, minute = map(int, time.split(":"))
            if not (0 <= hour < 24 and 0 <= minute < 60):
                raise forms.ValidationError("Enter a valid time in HH:MM format.")
        except ValueError:
            raise forms.ValidationError("Time should be in HH:MM format.")
        return time