from django.urls import path, include
from .views import solve_message, predict_charges, CustomLoginView, SignupView, HomeView, UserProfileView, AboutView, contact_view, JoinUsView, ApplyView, TemplateView, apply, contact_view, HealthAdvicesView, CybersecurityAwarenessView, message_list_view, ChangePasswordView, PredictChargesView
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views # easier to use

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('logout/', UserLogoutView.as_view(), name='logout_user'), 

    # For the users 
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('predict-charges/', PredictChargesView.as_view(), name='predict'),
    
    # Website other pages
    path('about/',AboutView.as_view(), name='about'),
    path('join-us/', JoinUsView.as_view(), name='join_us'),
    path('contact/', contact_view, name='contact'),
    path('apply/', ApplyView.as_view(), name='apply'),
    path('thank-you/', TemplateView.as_view(template_name='insurance_app/apply_thank_you.html'), name='apply_thank_you'), #thank you after applying a job
    path('health-advices/', HealthAdvicesView.as_view(), name='health_advices'),
    path('cybersecurity-awareness/',CybersecurityAwarenessView.as_view(), name='cybersecurity_awareness'),
    path('quote-predict/', predict_charges, name='predict_charges'),
    path('messages/', message_list_view, name='messages_list'),
    path('solve-message/<int:message_id>/', solve_message, name='solve_message'),
    
    # Reset password URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='insurance_app/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='insurance_app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='insurance_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='insurance_app/password_reset_complete.html'), name='password_reset_complete'),
    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'), # Other case



]