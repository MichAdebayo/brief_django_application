from django.urls import path, include
from .views import CustomLoginView, SignupView, HomeView, UserProfileView, AboutView, JoinUsView, ApplyView, TemplateView, apply,contact_view, HealthAdvicesView, CybersecurityAwarenessView, ChangePasswordView
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'), # REPLACE WITH DOROTHEE'S CODE
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('about/',AboutView.as_view(), name='about'),
    path('join-us/', JoinUsView.as_view(), name='join_us'),
    path('apply/', apply, name='apply'),
    path('apply/', ApplyView.as_view(), name='apply'),
    path('thank-you/', TemplateView.as_view(template_name='insurance_app/apply_thank_you.html'), name='apply_thank_you'),#thank you after applying a job
    path('contact/', contact_view, name='contact'),
    path('health-advices/', HealthAdvicesView.as_view(), name='health_advices'),
    path('cybersecurity-awareness/',CybersecurityAwarenessView.as_view(), name='cybersecurity_awareness'),
    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
]