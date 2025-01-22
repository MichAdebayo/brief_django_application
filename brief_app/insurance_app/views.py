# from django.shortcuts import render

from django.views.generic import ListView, FormView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import UserProfile
from .forms import UserProfileForm

# Create your views here.
class UserProfileView(FormView):
    model = UserProfile # Specify the model to use
    template_name = 'app/user_profile.html' # Specify the template
    context_object_name = 'users' # The name to use in the template
    form_class = UserProfileForm



