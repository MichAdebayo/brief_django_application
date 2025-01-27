from django.contrib import admin
from .models import UserProfile, Job, ContactMessage

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