from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.welcome, name='welcome'), #change the URL to '/home/'
]
