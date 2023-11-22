from django.shortcuts import render
from . import views
from page.models import Courses,College
import courses.views as courses_views
import json
# Create your views here.


def profiling_form_json():
    undergraduate=["pregrado",courses_views.get_courses_from_level("pregrado")]
    master=["maestría",courses_views.get_courses_from_level("maestría")]
    doctorate=["doctorado",courses_views.get_courses_from_level("doctorado")]
    levels=[undergraduate,master,doctorate]
    modalities=["presencial","online","hibrida","indiferente"]
    times=["200 horas o menos", "1.5 a 2.5 años", "2.5 a 4 años", "Más de 4 años"]
    labels=courses_views.get_all_labels
    greatest_price=courses_views.greatest_course_price()
    return {'levels':levels,'modalities':modalities, 'times':times,'labels':labels,'max_price':greatest_price}

def profiling_form(request):
    return render(request,'profiling_form.html',profiling_form_json())

def results(request):
    studies = request.POST.get("studies", "")
    undergraduate = request.POST.get("pregrado", "")
    master = request.POST.get("maestría", "")
    doctorate = request.POST.get("doctorado", "")
    modality = request.POST.get('modality',"")

    times_str = request.POST.get("times","")
    times_data = json.loads(times_str)
    times = times_data.get("times", [])

    courses_str = request.POST.get("courses", "")
    courses_data = json.loads(courses_str)
    courses = courses_data.get("courses", [])
    universities_str=request.POST.get("universities","")
    universities_data = json.loads(universities_str)
    universities = universities_data.get("universities", [])
    labels_str=request.POST.get("labels","")
    labels_data = json.loads(labels_str)
    labels = labels_data.get("labels", [])
    budget=request.POST.get("budget","")


    print("Estudios:", studies)
    print("Pregrado:", undergraduate)
    print("Maestria:", master)
    print("Doctorado:", doctorate)
    print("courses:", courses)
    print("Universities:", universities)
    print("Modalidad",modality)
    print("Tiempo",times)
    print("Labels",labels)
    print("Budget", budget)


    return render(request, "results.html")