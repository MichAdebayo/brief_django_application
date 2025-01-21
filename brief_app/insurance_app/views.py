
# Create your views here.
from django.shortcuts import render

def welcome(request):
    return render(request, 'insurance_app/welcome.html')
