from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'         # Template for the home page

class CustomLoginView(LoginView):
    template_name = 'login.html'        # Template for the login page
    redirect_authenticated_user = True  # Redirect already logged-in users
    def get_success_url(self):          # Redirect to a specific URL after login
        return reverse_lazy('home')     # Replace 'home' with the name of your desired URL
    
class SignupView(FormView):
    template_name = 'signup.html'       # Template for the signup page
    form_class = UserCreationForm       # Form to use for signup

    def form_valid(self, form):         # Save the user to the database
        user = form.save()              # Automatically log in the user after signup
        login(self.request, user)       # Redirect to the home page
        return redirect('home')

# Create your views here.
from django.shortcuts import render

def welcome(request):
    return render(request, 'insurance_app/welcome.html')
