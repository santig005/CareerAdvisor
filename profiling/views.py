from django.shortcuts import render
from . import views
from page.models import Courses,College
import courses.views as courses_views
import json
# Create your views here.

def profiling_form(request):
    undergraduate=["pregrado",courses_views.get_courses_from_level("pregrado")]
    master=["maestría",courses_views.get_courses_from_level("maestría")]
    doctorate=["doctorado",courses_views.get_courses_from_level("doctorado")]
    levels=[undergraduate,master,doctorate]
    return render(request,'profiling_form.html',{'levels':levels})

def results(request):
    estudios = request.POST.get("estudios", "")
    pregrado = request.POST.get("pregrado", "")
    maestria = request.POST.get("maestría", "")
    doctorado = request.POST.get("doctorado", "")
    cursos=request.POST.get("cursos","")
    universities=request.POST.get("universidades","")

    print("Estudios:", estudios)
    print("Pregrado:", pregrado)
    print("Maestria:", maestria)
    print("Doctorado:", doctorado)
    print("Cursos:", cursos)
    print("Universities:", universities)

    return render(request, "results.html")