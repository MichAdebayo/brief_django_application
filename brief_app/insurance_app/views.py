from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from .models import UserProfile, Job, ContactMessage
from .forms import UserProfileForm, UserSignupForm, ApplicationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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
    
    
# Create your views here.
class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'insurance_app/profile.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


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
    template_name = 'insurance_app/health_advices.html'

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
