from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView # LogoutView
from django.views.generic.edit import FormView
#from django.contrib.auth.forms import BaseUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import UserProfile
from .forms import UserProfileForm, UserSignupForm, UserLoginForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'insurance_app/home.html'         # Template for the home page

# class SignupView(FormView):
#     template_name = 'insurance_app/signup.html'       # Template for the signup page
#     form_class = CustomUserCreationForm       # Form to use for signup

#     def form_valid(self, form):         # Save the user to the database
#         user = form.save()              # Automatically log in the user after signup
#         login(self.request, user)       # Redirect to the home page
#         return redirect('login')

class SignupView(FormView):
    template_name = 'insurance_app/signup.html'
    form_class = UserSignupForm  # Utilisez un formulaire personnalisé
    redirect_authenticated_user = True  # Redirect already logged-in users
    success_url = reverse_lazy('login')

    # def form_valid(self, form):
    #     user = form.save()  # Enregistrez l'utilisateur
    #     login(self.request, user)  # Connectez automatiquement l'utilisateur
    #     return redirect('login')  # Redirigez vers la page de profil
    
class CustomLoginView(LoginView):
    template_name = 'insurance_app/login.html'        # Template for the login page
    form_class = UserLoginForm
    redirect_authenticated_user = True  # Redirect already logged-in users
    success_url = reverse_lazy('home')     # Replace 'home' with the name of your desired URL

# Create your views here.
class UserProfileView(FormView):
    model = UserProfile # Specify the model to use
    template_name = 'insurance_app/user_profile.html' # Specify the template
    context_object_name = 'users' # The name to use in the template
    form_class = UserProfileForm

# # Create your views here.
# from django.shortcuts import render

# def welcome(request):
#     return render(request, 'insurance_app/welcome.html')
# from django.shortcuts import render





