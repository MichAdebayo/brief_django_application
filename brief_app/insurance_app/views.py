from django.shortcuts import render, redirect 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView #, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import UserProfile, Job, ContactMessage
from .forms import UserProfileForm, UserSignupForm, UserLoginForm, ApplicationForm, ChangePasswordForm
from django.http import HttpResponse
import pickle
from django.http import JsonResponse
import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.views import View 


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


#templates  for Assur'Cares Section
class HealthAdvicesView(TemplateView):
    template_name = 'insurance_app/health_advices.html'


class CybersecurityAwarenessView(TemplateView):
    template_name = 'insurance_app/cybersecurity_awareness.html'


# Logic to save the application data (e.g., store it in the database or email it)
def apply(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        job_id = request.POST.get('job_id')
        resume = request.FILES.get('resume')

        return HttpResponse("Application submitted successfully!")
    return redirect('join_us')

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


#################################################################################
# REPLACE WITH DOROTHEE'S CODE

class SignupView(CreateView):
    model = UserProfile
    form_class = UserSignupForm  # Utilisez un formulaire personnalisé
    template_name = 'insurance_app/signup.html'
    success_url = reverse_lazy('test_login')
    # redirect_authenticated_user = True  # Redirect already logged-in users

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'insurance_app/login.html' 
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        # Authenticate the user
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            # Log in the user and redirect
            login(self.request, user)
            return super().form_valid(form)
        else:
            # Invalid credentials, show error message
            form.add_error(None, 'Invalid username or password.') # Add a general error message
            return self.form_invalid(form)

    def get_success_url(self):
        print("#########Get success URL called########")
        success_url =  reverse_lazy('home')
        return reverse_lazy('home')  # Redirect to a simple page

#################################################################################


# Template for user profile view
class UserProfileView(LoginRequiredMixin, UpdateView): 
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'insurance_app/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Return the UserProfile object for the logged-in user
        return self.request.user
    
    def form_valid(self, form):
            # Save the form and display a success message
            response = super().form_valid(form)
            messages.success(self.request, 'Your profile has been updated!')
            return response
    

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm  
    template_name = 'insurance_app/changepassword.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        # Save the new password
        response = super().form_valid(form)
        # Add a success message
        messages.success(self.request, 'Your password has been changed successfully!')
        return response


# class PredictChargesView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         # Fetch the user's profile data
#         user = request.user

#         # Prepare input data for the model
#         age = user.age
#         sex_encoded = 1 if user.sex == 'Male' else 0
#         bmi = user.weight / ((user.height / 100) ** 2)  # Calculate BMI
#         children = user.num_children
#         smoker_encoded = 1 if user.smoker == 'Yes' else 0

#         input_data = [[age, sex_encoded, bmi, children, smoker_encoded]]

#         # Load the ML model
#         model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
#         with open(model_path, 'rb') as f:
#             model = pickle.load(f)

#         # Predict charges
#         predicted_charges = model.predict(input_data)[0]

#         # Render the result
#         return render(request, 'predict_charges.html', {
#             'predicted_charges': round(predicted_charges, 2)
#         })




