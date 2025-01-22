from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'), #This is our welcome page'
]
