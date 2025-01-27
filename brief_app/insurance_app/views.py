from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView #, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import UserProfile, Job, ContactMessage
from .forms import UserProfileForm, UserSignupForm, UserLoginForm, ApplicationForm
from django.http import HttpResponse
import pickle
from django.http import JsonResponse
import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

# Create your views here.
class HomeView(TemplateView):
    template_name = 'insurance_app/home.html'   
          # Template for the home page

#template for about us 
class AboutView(TemplateView):
    template_name= 'insurance_app/about.html'
#Template for join us view 
class JoinUsView(TemplateView):
    template_name = 'insurance_app/join_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.all()
        return context
#### apply view for the join us view

class ApplyView(TemplateView):
    template_name = 'apply_thank_you.html'

    def post(self, request, *args, **kwargs):
        # Handle form submission here
        if request.method == 'POST':
            form = ApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                # Process the form (e.g., save data, send email, etc.)
                form.save()  # Save the application in our model 
                return redirect('apply_thank_you')  # Redirect to a thank you page
        else:
            form = ApplicationForm()
        
        return render(request, self.template_name, {'form': form})

# Logic to save the application data (e.g., store it in the database or email it)

def apply(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        job_id = request.POST.get('job_id')
        resume = request.FILES.get('resume')

        

        return HttpResponse("Application submitted successfully!")
    return redirect('join_us')

#class WelcomeView(TemplateView):
    #template_name = 'insurance_app/welcome.html'  
#templates  for Assur'Cares Section
class HealthAdvicesView(TemplateView):
    template_name = 'insurance_app/health_advices.html'

class CybersecurityAwarenessView(TemplateView):
    template_name = 'insurance_app/cybersecurity_awareness.html'

# class SignupView(CreateView):
#     model = UserProfile
#     form_class = UserSignupForm  # Utilisez un formulaire personnalisé
#     template_name = 'insurance_app/signup.html'
#     success_url = reverse_lazy('test_login')
#     print("###########Signup success###########")
#     # redirect_authenticated_user = True  # Redirect already logged-in users

#     def form_valid(self, form):         # Save the user to the database
#         self.object = form.save()
#         self.request.session['initial_user_profile'] = {
#             'username': self.object.username,
#             'email': self.object.email,
#         }
#         print("###########Form Valid success###########")
#         return super().form_valid(form)

# class TestLoginView(LoginView):
#     template_name = 'insurance_app/login.html'  # Or a simple test template
#     redirect_authenticated_user = True
#     print("###########Login Page success###########")
#     success_url =  reverse_lazy('home')
#     print("###########I can go home###########")

#     def get_success_url(self):
#         print("#########Get success URL called########")
#         success_url =  reverse_lazy('home')
#         return reverse_lazy('home')  # Redirect to a simple page
    
class CustomLoginView(LoginView):
    #form_class = UserLoginForm
    template_name = 'insurance_app/login.html'  # Template for the login page
    success_url = reverse_lazy('home')     # Replace 'home' with the name of your desired URL
    redirect_authenticated_user = True  # Redirect already logged-in users

# Create your views here.
class UserProfileView(UpdateView): # LoginRequiredMixin, 
    model = UserProfile # Specify the model to use
    form_class = UserProfileForm
    template_name = 'insurance_app/user_profile.html' # Specify the template

    # def get_success_url(self):
    #      return reverse_lazy('user_profile', kwargs={'pk': self.request.user.pk})
    
    # redirect_authenticated_user = True

    # def get_initial(self):
    #     initial = super().get_initial()
    #     if 'initial_user_profile' in self.request.session:
    #         initial.update(self.request.session.pop('initial_user_profile'))
    #         self.request.session.modified = True
    #     return initial
    
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     messages.success(self.request, 'Your profile has been updated!')
    #     return response
  
    def get_object(self, queryset=None):
        return self.request.user.userprofile




#To handle the messages submission
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save the message to the database
        ContactMessage.objects.create(name=name, email=email, message=message)
        
        # Show a success message
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')  # Replace 'contact' with the name of your URL pattern
    
    return render(request, "insurance_app/contact_form.html")



