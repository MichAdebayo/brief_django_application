from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from .models import UserProfile, Job, ContactMessage
from .forms import UserProfileForm, UserSignupForm, ApplicationForm, ChangePasswordForm, PredictChargesForm
from django.http import HttpResponse
import pickle
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from django.views import View 
import pandas as pd
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
class HomeView(TemplateView):
    template_name = 'insurance_app/home.html'           # Template for the home page

    def get_context_data(self, **kwargs):
        # Récupérer le contexte du template
        context = super().get_context_data(**kwargs)

        # Sections de l'Info Bar
        context['info_bar_sections'] = [
            {
                'title': 'Assur\'Aimant',
                'links': [
                    {'name': 'About Us', 'url': reverse('about')},
                    {'name': 'Join Us', 'url': reverse('join_us')},
                ]
            },
            {
                'title': 'Assur\'Cares',
                'links': [
                    {'name': 'Need a Quote', 'url': reverse('join_us')},
                    {'name': 'Need Help', 'url': reverse('contact')},
                ]
            },
            {
                'title': 'Assur\'Awareness',
                'links': [
                    {'name': 'Health Advice', 'url': reverse('health_advices')},
                    {'name': 'Cybersecurity Awareness', 'url': reverse('cybersecurity_awareness')},
                ]
            }
        ]

        return context

class SignupView(CreateView):                           # Generic view for creating an object
    model = UserProfile                                 # Model used
    form_class = UserSignupForm                         # Form used
    template_name = 'insurance_app/signup.html'         # HTML template for displaying the form
    success_url = reverse_lazy('login')                 # Redirect after successful signup

    
class CustomLoginView(LoginView):
    template_name = 'insurance_app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Redirect to the profile page after successful login
        return reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to the profile page
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Check if 'remember me' is checked
        remember_me = self.request.POST.get('remember_me', None) is not None

        # Set session expiry accordingly
        if not remember_me:
            self.request.session.set_expiry(0)  # Expire session on browser close
        else:
            self.request.session.set_expiry(1209600)  # Session lasts 2 weeks

        return super().form_valid(form)


# Template Eliandy
## Template for about us 
class AboutView(TemplateView):
    template_name= 'insurance_app/about.html'
    
## Template for join us view 
class JoinUsView(TemplateView):
    template_name = 'insurance_app/join_us.html'
    # apply view for the join us view
    def get_context_data(self, **kwargs):                       
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.all()
        return context
    
## Template for join us view 
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

class HealthAdvicesView(TemplateView):
    template_name = 'insurance_app/health_advices.html'  # Assur'Cares Section View Template

class CybersecurityAwarenessView(TemplateView):
    template_name = 'insurance_app/cybersecurity_awareness.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

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

# To solve the messages
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


# Dynamic quote :
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


# Template for user profile view
class UserProfileView(LoginRequiredMixin, UpdateView): 
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'insurance_app/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Return the UserProfile object for the logged-in user
        print(self.request.user)
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
    

class PredictChargesView(LoginRequiredMixin, UpdateView): 
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'insurance_app/predict.html'
    success_url = reverse_lazy('predict')

    def get_object(self, queryset=None):
        # Return the UserProfile object for the logged-in user
        print(self.request.user)
        return self.request.user
    
    def form_valid(self, form):
            # Save the form and display a success message
            response = super().form_valid(form)
            messages.success(self.request, 'Your charges has been updated!')
            return response
