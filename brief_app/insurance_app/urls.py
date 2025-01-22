from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
]