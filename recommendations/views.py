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

undergraduate_require=["high_school","undergraduate"]
specialization_require=["high_school","undergraduate","specialization"]
master_require=["high_school","undergraduate","master"]
doctorate_require=["high_school","undergraduate","master","doctorate"]
# now in spanish
bachillerato_require=["bachillerato"]
pregrado_require=["bachillerato","pregrado"]
especializacion_require=["bachillerato","pregrado","especialización"]
maestria_require=["bachillerato","pregrado","especialización","maestría"]

class recommendation_form():
    def __init__(self,form):
        self.idapplicant=form.idapplicant
        self.studies=form.studies
        self.preferences=form.preferences
        self.interest=form.interest
    
    def default_search(self):
        compatible_courses=[]
        allcourses=Courses.objects.all()
        posi_levels=[]
        exclude_courses=[]
        max_study=""
        if self.studies["doctorate"]:
            max_study="doctorado"
        elif self.studies["master"]:
            max_study="maestría"
        elif self.studies["specialization"]:
            max_study="especialización"
        elif self.studies["undergraduate"]:
            max_study="pregrado"
        elif self.studies["high_school"]:
            max_study="bachillerato"

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
        
        print(self.preferences["times"])
        print(posi_levels)
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
        for course in self.studies["courses"]:
            item=Courses.objects.filter(idcourse=course)[0]
            exclude_courses.append(item.idcourse)
        for course in allcourses:
            if course.academic_level in posi_levels and course.modality==self.preferences["modality"] and course not in exclude_courses:
                print(course.name)
                compatible_courses.append(course)
        return compatible_courses
        

    @abstractmethod
    def get_courses(self):
        pass
    
#Ahora una clase que lo implementa
class default_recommendation(recommendation_form):
    def __init__(self,form):
        super().__init__(form)
    def get_courses(self):
        return self.default_search()
    
class embedding_recommendation(recommendation_form):
    def __init__(self,form):
        super().__init__(form)
    def get_courses(self):
        default_courses=self.default_search()
        colleges=""
        courses=""
        labels=""
        for college in self.studies["colleges"]:
            item=College.objects.filter(idcollege=college)[0]
            colleges+=item.name+", "
        for course in self.studies["courses"]:
            item=Courses.objects.filter(idcourse=course)[0]
            courses+=item.name+", "
        for label in self.interest["labels"]:
            labels+=label+", "
        description=colleges+courses+labels
        _ = load_dotenv('openAI.env')
        openai.api_key  = os.environ['openAI_api_key']
        emb_req = get_embedding(description,engine='text-embedding-ada-002')
        items=default_courses
        print("Emb generado")
        print(emb_req)
        sim = []
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
            i.match=similarity
            similarity_list.append((i, similarity))
            '''sim.append(similarity)
        sim = np.array(sim)
        idx = np.argmax(sim)
        idx = int(idx)
        respuesta=[(items[idx])]'''
        # Ordenar la lista de similitud de mayor a menor
        similarity_list.sort(key=lambda x: x[1], reverse=True)

        # Obtener la respuesta con todos los elementos ordenados
        respuesta = [item for item, _ in similarity_list]
        for r in respuesta:
            print(r.name)
            print(r.match)



def results(request,profile_form):
    print("Entro a resultados")
    recommend=default_recommendation(profile_form)
    print(recommend.default_search())
    emb_recommend=embedding_recommendation(profile_form)
    print(emb_recommend.get_courses())
    return render(request,'results.html')
