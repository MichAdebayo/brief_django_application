from django.urls import path, include
from .views import solve_message,predict_charges,CustomLoginView, SignupView, HomeView, UserProfileView,WelcomeView,AboutView, JoinUsView,ApplyView,TemplateView,apply,contact_view,HealthAdvicesView,CybersecurityAwarenessView,message_list_view
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/',CustomLoginView.as_view() , name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    path('welcome/',WelcomeView.as_view(), name='welcome'),
    path('about/',AboutView.as_view(), name='about'),
    path('join-us/', JoinUsView.as_view(), name='join_us'),
    path('apply/', apply, name='apply'),
    path('apply/', ApplyView.as_view(), name='apply'),
    path('thank-you/', TemplateView.as_view(template_name='insurance_app/apply_thank_you.html'), name='apply_thank_you'),#thank you after applying a job
    path('contact/', contact_view, name='contact'),
    path('health-advices/', HealthAdvicesView.as_view(), name='health_advices'),
    path('cybersecurity-awareness/',CybersecurityAwarenessView.as_view(), name='cybersecurity_awareness'),
    path('messages/', message_list_view, name='messages_list'),
    path('solve-message/<int:message_id>/', solve_message, name='solve_message'),
    path('predict/', predict_charges, name='predict_charges'),

# path("__reload__/", include("django_browser_reload.urls")),
]
