# from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView #, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import UserProfile
from .forms import UserProfileForm, UserSignupForm, UserLoginForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'insurance_app/home.html'         # Template for the home page

class SignupView(CreateView):
    model = UserProfile
    form_class = UserSignupForm  # Utilisez un formulaire personnalisé
    template_name = 'insurance_app/signup.html'
    success_url = reverse_lazy('login')
    redirect_authenticated_user = True  # Redirect already logged-in users

    def form_valid(self, form):         # Save the user to the database
        self.object = form.save()
        self.request.session['initial_user_profile'] = {
            'username': self.object.username,
            'email': self.object.email,
            'password' : self.object.password,
        }
        return super().form_valid(form)

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'insurance_app/login.html'  # Template for the login page
    success_url = reverse_lazy('home')     # Replace 'home' with the name of your desired URL
    redirect_authenticated_user = True  # Redirect already logged-in users

# Create your views here.
class UserProfileView(UpdateView): # LoginRequiredMixin, 
    model = UserProfile # Specify the model to use
    form_class = UserProfileForm
    template_name = 'insurance_app/user_profile.html' # Specify the template
    success_url = reverse_lazy('user_profile') 
    # redirect_authenticated_user = True

    def get_initial(self):
        initial = super().get_initial()
        if 'initial_user_profile' in self.request.session:
            initial.update(self.request.session.pop('initial_user_profile'))
            self.request.session.modified = True
        return initial
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your profile has been updated!')
        return response
  
    def get_object(self, queryset=None):
        return self.request.user.userprofile








