from django.shortcuts import render
from page.models import Courses, College
# Create your views here.
from dotenv import load_dotenv, find_dotenv
import json
import os
import time
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np

# Get the greastest price of the courses
def greatest_course_price():
    allcourses = Courses.objects.order_by('-price')
    return allcourses[0].price

# The next function gets the set of different course names
def get_unique_course_names(level):
    allcourses = Courses.objects.filter(academic_level=level).values()
    course_names_set = set(course['name'] for course in allcourses)
    course_names_list = list(course_names_set)
    return course_names_list

# The next function gets the set of colleges that provide a course
def get_provider_colleges(course_name):
    named_courses=Courses.objects.filter(name=course_name)
    provided_by=set()
    for n in named_courses:
        college=College.objects.filter(idcollege=n.college_idcollege_id)[0]
        provided_by.add(college)
    provided_by=list(provided_by)
    return provided_by

# The next function gets the set of courses with different name as well as the group of colleges that provide that course
def get_courses_from_level(level):
    course_names_list = get_unique_course_names(level)
    unique_courses=[]
    for course_name in course_names_list:
        named_courses=Courses.objects.filter(name=course_name)
        trivial_course=named_courses[0]
        colleges=get_provider_colleges(course_name)
        trivial_course.universities=colleges
        unique_courses.append(trivial_course)
    return unique_courses

def get_all_labels():
    labels=set()
    for course in Courses.objects.all():
        course_labels=course.get_labels()
        for label in course_labels:
            labels.add(label)
    labels=list(labels)
    labels.sort()
    return labels

def create_embeddings():
    _ = load_dotenv('openAI.env')
    print(_)
    print("Paso 1")
    openai.api_key  = os.environ['openAI_api_key']
    print("Paso 2")
    with open('output_g.json', 'r') as file:
        file_content = file.read()
        courses = json.loads(file_content)
    print("Paso 3")

    #Vamos a crear una nueva llave con el embedding de la descripción de cada curso en el archivo .json
    for i in range(len(courses)):
        print(f"Vamos a generar el "+str(i))
        emb = get_embedding(courses[i]['description'],engine='text-embedding-ada-002')
        print(emb)
        print("duermo")
        time.sleep(20)
        print("Generado el ",str(i))
        courses[i]['embedding'] = emb
    print("Paso 5")
    #Vamos a almacenar esta información en un nuevo archivo .json
    with open('course_descriptions_embeddings.json', 'w') as json_file:
        json.dump(courses, json_file, indent=2)
        

def add_embeddings_db():
    json_file_path = 'course_descriptions_embeddings.json'
    # Load data from the JSON file
    with open(json_file_path, 'r') as file:
        courses = json.load(file)       
    for course in courses:
        print(f'curso '+ str(course["idcourse"]))
        emb = course['embedding']
        emb_binary = np.array(emb).tobytes()
        item = Courses.objects.filter(idcourse = course['idcourse']).first()
        print(len(emb_binary))
        #if item.emb:
        #   print(item.emb)
        #   print("tiene emb")
        #   break
        #item.emb = emb_binary
        #item.save()

def add_descriptions_to_courses():
    json_file_path = 'output_g.json'
    # Load data from the JSON file
    with open(json_file_path, 'r') as file:
        courses = json.load(file)
    for course in courses:
        existance=Courses.objects.filter(idcourse=course['idcourse']).first()
        if not existance.description:
            existance.description=course['description']
            existance.save()
    
def prueba_emb():
    with open('course_descriptions_embeddings.json', 'r') as file:
        file_content = file.read()
        courses = json.loads(file_content)
        #Para saber cuáles cursos se parecen más, podemos hacer lo siguiente:
    print(courses[0]['name'])
    print(courses[2]['name'])
    for course in courses:
        print(f"Similitud entre curso {courses[0]['name']} y {course['name']}: {cosine_similarity(courses[0]['embedding'],course['embedding'])}")

    #Calculamos la similitud de coseno entre los embeddings de las descripciones de las cursos. Entre más alta la similitud
    #más parecidas las cursos.
    
def save_course_names_and_labels(output_file):
    all_courses = Courses.objects.all()
    course_data=[]
    # Extract unique course names and labels
    for course in all_courses:
        labels=course.get_labels()
        college=College.objects.filter(idcollege=course.college_idcollege_id)[0]
        description=course.name+", "+college.name
        for label in labels:
            description=description+", "+label
        course_data.append({'idcourse':course.idcourse,'college':college.idcollege,'name': course.name, 'description': description})
    print(course_data)
    
    # Save to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(course_data, json_file, indent=2)
    add_descriptions_to_courses()



def allcourses(request):
    output_json_file = "output_g.json"
    #save_course_names_and_labels(output_json_file)
    #create_embeddings()
    #add_embeddings_db()
    prueba_emb()
    return render(request,'courses.html')

