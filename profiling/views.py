from django.shortcuts import render
from . import views

# Create your views here.
def profiling_form(request):
    return render(request,'profiling_form.html')

def results(request):
    return render(request,'results.html')