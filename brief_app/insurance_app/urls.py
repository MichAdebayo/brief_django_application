<<<<<<< HEAD
from django.urls import path, include
from .views import CustomLoginView, SignupView, HomeView
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/',CustomLoginView.as_view() , name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("__reload__/", include("django_browser_reload.urls")),
]

=======
from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'), #This is our welcome page'
]
>>>>>>> origin/accueil
