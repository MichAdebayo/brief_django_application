from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import UserProfile
from .forms import UserProfileForm, UserSignupForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'insurance_app/home.html'           # Template for the home page

class SignupView(CreateView):                           # Generic view for creating an object
    model = UserProfile                                 # Model used
    form_class = UserSignupForm                         # Form used
    template_name = 'insurance_app/signup.html'         # HTML template for displaying the form
    success_url = reverse_lazy('login')                 # Redirect after successful signup

    
class CustomLoginView(LoginView):
    template_name = 'insurance_app/login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        # Redirect to the profile page after successful login
        return reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to the profile page
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)
    
# class CustomLogoutView(View):
#     """
#     CustomLogoutView handles the logout process for authenticated users.
#     It logs out the user and redirects them to a specified URL.
#     """

#     def get(self, request, *args, **kwargs):
#         """
#         Handles GET requests to log out the user.

#         Args:
#             request: The HTTP request object.
#             *args: Additional positional arguments.
#             **kwargs: Additional keyword arguments.

#         Returns:
#             A redirect to the URL specified after logout.
#         """
#         # Log out the user using Django's built-in logout function
#         logout(request)

#         # Redirect the user to the home page or any other URL
#         return redirect('/')
    
# Create your views here.
class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'insurance_app/profile.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user








