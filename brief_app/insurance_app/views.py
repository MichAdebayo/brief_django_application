from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView #, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import UserProfile, Job, ContactMessage
from .forms import UserProfileForm, UserSignupForm, UserLoginForm, ApplicationForm,InsuranceForm
from django.http import HttpResponse
import pickle
from django.http import JsonResponse
import json
import numpy as np
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.admin.views.decorators import staff_member_required
import pickle
import pandas as pd

import pickle





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

#Welcome view (used to modified homepage)
class WelcomeView(TemplateView):
    template_name = 'insurance_app/welcome.html'  

#templates  for Assur'Cares Section
class HealthAdvicesView(TemplateView):
    template_name = 'insurance_app/health_advices.html'

class CybersecurityAwarenessView(TemplateView):
    template_name = 'insurance_app/cybersecurity_awareness.html'

#Sign up view 
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
    #form_class = UserLoginForm
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


# To see this messages 
@staff_member_required
def message_list_view(request):
    messages = ContactMessage.objects.all().order_by('-submitted_at')  # Most recent first
    return render(request, "insurance_app/messages_list.html", {"messages": messages})


# to solve the messages

@csrf_exempt
def solve_message(request, message_id):
    if request.method == 'POST':
        try:
            contact_message = ContactMessage.objects.get(id=message_id)
            contact_message.delete()
            return JsonResponse({'success': True})
        except ContactMessage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


#Dynamic quote : 

def predict_charges(request):
    prediction = None

    # Handle the GET request - Render the form
    if request.method == 'GET':
        return render(request, 'insurance_app/insurance_form.html', {'prediction': prediction})

    # Handle the POST request - Process the form data and predict
    elif request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extract data from the JSON
            height = float(data.get('height'))
            weight = float(data.get('weight'))
            age = int(data.get('age'))
            sex = data.get('sex')
            smoker = data.get('smoker')
            region = data.get('region')
            children = int(data.get('children'))
            bmi = float(data.get('bmi'))
            bmi_category = data.get('bmi_category')

            # Load model from pickle
            model_path = 'insurance_app/model/model_1.pickle'
            with open(model_path, 'rb') as file:
                model = pickle.load(file)

            # Prepare data as a DataFrame (ensure the order matches your model's expected input)
            input_data = pd.DataFrame([{
                'height': height,
                'weight': weight,
                'age': age,
                'sex': sex,
                'smoker': smoker,
                'region': region,
                'children': children,
                'bmi': bmi,
                'BMI_category': bmi_category
            }])

            # Make the prediction
            prediction = round(model.predict(input_data)[0], 2)

            # Ensure prediction is non-negative
            prediction = max(prediction, 0)

            # Return prediction as JSON response
            return JsonResponse({'prediction': prediction})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # If not GET or POST, return an error
    return JsonResponse({'error': 'Invalid request method'}, status=405)
