from django.shortcuts import render
from page.models import Courses, College
# Create your views here.


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

def allcourses(request):
    return render(request,'courses.html')