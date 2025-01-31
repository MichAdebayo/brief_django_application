from django.contrib import admin
from .models import UserProfile, Job, ContactMessage, Availability
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.forms.widgets import DateInput
from datetime import datetime



# Register your models here.
admin.site.register(UserProfile)


#Job listing
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'experience')


#Contact messages
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('submitted_at',)


###availability#####
class AvailabilityAdminForm(forms.ModelForm):
    TIME_CHOICES = [(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(9, 19)]  # 09:00 - 18:00

    time_slots = forms.MultipleChoiceField(choices=TIME_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Availability
        fields = ['date', 'time_slots']

    def clean_time_slots(self):
        return self.cleaned_data['time_slots']  # Ensure list format

class AvailabilityAdmin(admin.ModelAdmin):
    form = AvailabilityAdminForm
    list_display = ['date', 'display_times']

    def display_times(self, obj):
        return ", ".join(obj.time_slots)

admin.site.register(Availability, AvailabilityAdmin)


# admin.py
from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason', 'date', 'time')  # Fields to display in the list view
    list_filter = ('reason', 'date')  # Add filter options
    search_fields = ('user__username', 'reason', 'date')  # Add search functionality
    date_hierarchy = 'date'  # Allows for filtering by date in a hierarchy
    ordering = ('-date',)  # Order by date descending (most recent first)

    # Optionally, you can add formfield customization
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'time':
            kwargs['choices'] = [(f"{hour:02}:00", f"{hour:02}:00") for hour in range(9, 19)]  # Time choices from 09:00 to 18:00
        return super().formfield_for_choice_field(db_field, request, **kwargs)

# Register the model and custom admin
admin.site.register(Appointment, AppointmentAdmin)
