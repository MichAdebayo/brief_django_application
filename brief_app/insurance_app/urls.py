from django.urls import path, include
from .views import (solve_message,predict_charges,CustomLoginView, SignupView, HomeView, UserProfileView, AboutView, 
                    JoinUsView, ApplyView, TemplateView, apply,contact_view, 
                    HealthAdvicesView, CybersecurityAwarenessView,message_list_view, ChangePasswordView, 
                    PredictChargesView, UserLogoutView, WelcomeView, PredictionHistoryView)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'), # REPLACE WITH DOROTHEE'S CODE
    path('login/', CustomLoginView.as_view(), name='login'), # REPLACE WITH DOROTHEE'S CODE
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('about/',AboutView.as_view(), name='about'),
    path('join-us/', JoinUsView.as_view(), name='join_us'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('apply/', apply, name='apply'),
    path('contact/', contact_view, name='contact'),
    path('apply/', ApplyView.as_view(), name='apply'),
    path('thank-you/', TemplateView.as_view(template_name='insurance_app/apply_thank_you.html'), name='apply_thank_you'), #thank you after applying a job
    path('health-advices/', HealthAdvicesView.as_view(), name='health_advices'),
    path('cybersecurity-awareness/',CybersecurityAwarenessView.as_view(), name='cybersecurity_awareness'),
    path('messages/', message_list_view, name='messages_list'),
    path('solve-message/<int:message_id>/', solve_message, name='solve_message'),
    path('quote-predict/', predict_charges, name='predict_charges'),
    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('predict-charges/', PredictChargesView.as_view(), name='predict'),
    path('logout/', UserLogoutView.as_view(), name='logout_user'), 
    path('prediction-history/', PredictionHistoryView.as_view(), name='prediction_history'),
]