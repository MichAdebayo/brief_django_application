from django import forms
from .models import UserProfile
from .models import JobApplication, Appointment, Availability # Assuming you have a JobApplication model to store applications
from django.utils.html import format_html
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password

class PredictChargesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['smoker', 'age', 'weight', 'height', 'num_children']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username',
                  'email', 'smoker', 'region', 'sex', 'num_children',
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


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication  # This will be the model for storing application data
        fields = ['name', 'email', 'resume', 'cover_letter']

    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    resume = forms.FileField(required=False)
    cover_letter = forms.CharField(widget=forms.Textarea, required=True)


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize labels
        self.fields['old_password'].label = "Current Password"
        self.fields['new_password1'].label = "New Password"
        self.fields['new_password2'].label = "Confirm New Password"

        # Add help text for password requirements
        self.fields['new_password1'].help_text = format_html(
            '<ul class="text-sm text-gray-600 mt-2">'
            '<li>Your password must be at least 8 characters long.</li>'
            '<li>Your password cannot be entirely numeric.</li>'
            '<li>Your password cannot be too similar to your other personal information.</li>'
            '</ul>'
        )

        # Add Tailwind CSS classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-400',
            })



class AppointmentForm(forms.ModelForm):
    # Time slot choices (morning, afternoon)
    time_slot = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Appointment
        fields = ['availability', 'time_slot', 'reason']
        widgets = {
            'availability': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show only available dates (those with is_available=True)
        self.fields['availability'].queryset = Availability.objects.filter(is_available=True)

        # Dynamically populate the time_slot field based on the selected availability date
        if 'availability' in self.data:
            try:
                availability_id = int(self.data.get('availability'))
                availability = Availability.objects.get(id=availability_id)
                available_slots = self.get_available_time_slots(availability)
                self.fields['time_slot'].choices = [(slot, slot) for slot in available_slots]
            except (ValueError, Availability.DoesNotExist):
                pass

    def clean_availability(self):
        """Check if the selected availability date is already booked."""
        selected_date = self.cleaned_data.get('availability')
        if Appointment.objects.filter(availability=selected_date).exists():
            raise forms.ValidationError("This date is already booked. Please choose another one.")
        return selected_date

    def clean_time_slot(self):
        """Ensure that the selected time_slot is available for the selected date."""
        availability = self.cleaned_data.get('availability')
        time_slot = self.cleaned_data.get('time_slot')

        # Check if the selected time_slot exists for the selected availability
        if not Availability.objects.filter(date=availability, time_slot=time_slot, is_available=True).exists():
            raise forms.ValidationError(f"The selected time slot {time_slot} is not available for this date.")
        return time_slot

    def get_available_time_slots(self, availability):
        """Retrieve available time slots dynamically from the Availability model."""
        return [availability.time_slot for availability in Availability.objects.filter(date=availability.date, is_available=True)]