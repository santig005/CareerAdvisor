from django.shortcuts import render,get_object_or_404
from . import views
from page.models import Courses,College,Applicant,Profiling
import courses.views as courses_views
import recommendations.views as recommendations_views
import json
# Create your views here.

class form():
    def __init__(self,idapplicant,studies,preferences,interest):
        self.idapplicant=idapplicant
        self.studies=studies
        self.preferences=preferences
        self.interest=interest

def profiling_form_json():
    undergraduate=["pregrado",courses_views.get_courses_from_level("pregrado")]
    specialization=["especialización",courses_views.get_courses_from_level("especialización")]
    master=["maestría",courses_views.get_courses_from_level("maestría")]
    doctorate=["doctorado",courses_views.get_courses_from_level("doctorado")]

    levels=[undergraduate,specialization,master,doctorate]
    modalities=["presencial","online","hibrida","indiferente"]
    times=["200 horas o menos", "0.5 a 3.5 años", "Más de 4 años"]
    labels=courses_views.get_all_labels()
    greatest_price=courses_views.greatest_course_price()
    return {'levels':levels,'modalities':modalities, 'times':times,'labels':labels,'max_price':greatest_price}

def profiling_form(request):
    return render(request,'profiling_form.html',profiling_form_json())

def get_from_request(request,key):
    return request.POST.get(key,"")

def get_array_from_request(request,key):
    array_str=request.POST.get(key,"")
    array_data = json.loads(array_str)
    array = array_data.get(key, [])
    return array

def response(request):
    name=get_from_request(request,"name")
    email=get_from_request(request,"email")
    age=get_from_request(request,"age")
    if not name or not email or not age:
        print("Hay campo(s) sin llenar")
    

    modality=get_from_request(request,"modality")
    budget=get_from_request(request,"budget")
    times=get_array_from_request(request,"times")

    studies=get_from_request(request,"studies")
    high_school=get_from_request(request,"Bachillerato")
    undergraduate=get_from_request(request,"pregrado")
    specialization=get_from_request(request,"especialización")
    master=get_from_request(request,"maestría")
    doctorate=get_from_request(request,"doctorado")
    courses=get_array_from_request(request,"courses")
    universities=get_array_from_request(request,"universities")
    labels=get_array_from_request(request,"labels")
    
    # We add the results to a json file called results
    results = {}

    results["response"]={}
    results["response"]["studies"]={"high_school":high_school,"undergraduate":undergraduate,"specialization":specialization,"colleges":universities,"master":master,"doctorate":doctorate,"courses":courses}
    results["response"]["preferences"]={"budget":budget,"modality":modality,"times":times}
    results["response"]["interest"]={"labels":labels}

    with open('results.json', 'w') as file:
        json.dump(results, file,indent=1)
        
    #ahora leemos e imprimos los datos del json
    with open('results.json', 'r') as file:
        file_content = file.read()
        results = json.loads(file_content)
    
    exist=Applicant.objects.filter(email=email)
    if exist:
        print("El correo ya existe")
        idapplicant=exist[0].idapplicant
    else:
        print("voy a crear aplicante")
        Applicant.objects.create(
            name=name,
            email=email,
            age=age
        )
        item=Applicant.objects.get(email=email)
        idapplicant=item.idapplicant
    person=get_object_or_404(Applicant,idapplicant=idapplicant)
    Profiling.objects.create(
        applicant_idappilicant=person,
        studies=results["response"]["studies"],
        preferences=results["response"]["preferences"],
        interest=results["response"]["interest"],
    )
    profile_form=Profiling.objects.filter(applicant_idappilicant=person).last()
    new_form=form(profile_form.applicant_idappilicant,profile_form.studies,profile_form.preferences,profile_form.interest)
    recommended=recommendations_views.emb_results(request,new_form)
    for course in recommended:
        college = College.objects.filter(idcollege=course.college_idcollege_id)[0]
        course.college = college
    recommended=recommended[:6]
    return render(request,'results.html',{"allcourses":recommended})