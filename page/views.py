from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from .models import *

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')
