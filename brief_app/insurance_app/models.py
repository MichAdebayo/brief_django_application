from django.db import models
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class Login_and_SignUp(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    

class SignUp(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    surname_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=200)
    smoker = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    weight = models.CharField(max_length=200)
    height = models.CharField(max_length=200) 
    sex = models.CharField(max_length=200)
    user_name = models.ForeignKey(Login_and_SignUp, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.user_name
    
<<<<<<< HEAD
=======

class SignUp(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


>>>>>>> origin/accueil
