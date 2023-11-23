from django.shortcuts import render
from . import views
from page.models import Courses,College
import courses.views as courses_views
import json
import os
from abc import abstractmethod
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np

from dotenv import load_dotenv, find_dotenv
# Create your views here.


#this function determines the greatest level of study
def max_study_function(studies):
    max_study=""
    if studies["doctorate"]:
        max_study="doctorado"
    elif studies["master"]:
        max_study="maestría"
    elif studies["specialization"]:
        max_study="especialización"
    elif studies["undergraduate"]:
        max_study="pregrado"
    elif studies["high_school"]:
        max_study="bachillerato"
    return max_study

#this function determines the possible levels of study
def possible_level_function(max_study):
    posi_levels=[]
    if max_study=="especialización":
        posi_levels=["diplomado","pregrado","especialización","maestría"]
    elif max_study=="maestría" or max_study=="doctorado":
        posi_levels=["diplomado","pregrado","especialización","maestría","doctorado"]
    elif max_study=="pregrado":
        posi_levels=["diplomado","pregrado","especialización","maestría"]
    elif max_study=="bachillerato":
        posi_levels=["diplomado","pregrado"]
    else:
        posi_levels=["diplomado"]
    return posi_levels

def exclude_courses_function(studies):
    exclude_courses=[]
    for course in studies["courses"]:
        item=Courses.objects.filter(idcourse=course)[0]
        same_name=Courses.objects.all().filter(name=item.name)
        for s in same_name:
            exclude_courses.append(s.idcourse)
    return exclude_courses

class recommendation_form():
    def __init__(self,form):
        self.idapplicant=form.idapplicant
        self.studies=form.studies
        self.preferences=form.preferences
        self.interest=form.interest
    
    def default_search(self):
        allcourses=Courses.objects.all()
        max_study=max_study_function(self.studies)
        posi_levels=possible_level_function(max_study)
        compatible_courses=[]
        if "200 horas o menos" not in self.preferences["times"]:
            if "diplomado" in posi_levels:
                posi_levels.remove("diplomado")
        if "0.5 a 3.5 años" not in self.preferences["times"]:
            if "especialización" in posi_levels:
                posi_levels.remove("especialización")
            if "maestría" in posi_levels:
                posi_levels.remove("maestría")
        if "Más de 4 años" not in self.preferences["times"]:
            if "doctorado" in posi_levels:
                posi_levels.remove("doctorado")
            if "pregrado" in posi_levels:
                posi_levels.remove("pregrado")

        exclude_courses=exclude_courses_function(self.studies)
        for course in allcourses:
            if course.academic_level in posi_levels and course.modality==self.preferences["modality"] and course.idcourse not in exclude_courses and course.price<int(self.preferences["budget"]):
                compatible_courses.append(course)
        return compatible_courses

    @abstractmethod
    def get_courses(self):
        pass
    

class default_recommendation(recommendation_form):
    def __init__(self,form):
        super().__init__(form)
    def get_courses(self):
        return self.default_search()

def closest_results(description,courses):
    _ = load_dotenv('openAI.env')
    openai.api_key  = os.environ['openAI_api_key']
    emb_req = get_embedding(description,engine='text-embedding-ada-002')
    items=courses
    similarity_list = []
    for i in items:
        with open('course_descriptions_embeddings.json', 'r') as file:
            file_content = file.read()
            courses = json.loads(file_content)
        for j in courses:
            if j["idcourse"]==i.idcourse:
                i.emb=j["embedding"]
        emb = i.emb
        similarity=cosine_similarity(emb,emb_req)
        i.match=round((similarity*100),2)
        similarity_list.append((i, similarity))
    similarity_list.sort(key=lambda x: x[1], reverse=True)
    respuesta = [item for item, _ in similarity_list]
    return respuesta

    
class embedding_recommendation(recommendation_form):
    def __init__(self,form):
        super().__init__(form)
    def get_courses(self):
        default_courses=self.default_search()
        colleges=""
        courses=""
        label_array=set()
        labels=""
        for college in self.studies["colleges"]:
            item=College.objects.filter(idcollege=college)[0]
            colleges+=item.name+", "
        for course in self.studies["courses"]:
            item=Courses.objects.filter(idcourse=course)[0]
            courses+=item.name+", "
            course_labels=item.get_labels()
            for label in course_labels:
                label_array.add(label)
        for label in self.interest["labels"]:
            label_array.add(label)
        label_array=list(label_array)
        for label in label_array:
            labels+=label+", "
        description=colleges+courses+labels
        return closest_results(description,default_courses)



def results(request,profile_form):
    recommend=default_recommendation(profile_form)
    recommended=recommend.get_courses()
    return recommended
def emb_results(request,profile_form):
    emb_recommend=embedding_recommendation(profile_form)
    recommended=emb_recommend.get_courses()
    return recommended
