from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from .models import *

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def perfilamiento(request):
    return render(request,'perfilamiento.html')

def programas(request):
    return render(request,'cursos.html')
def resultados(request):
    return render(request, 'resultados.html')
def login(request):
    return render(request, 'login.html')
