from django.shortcuts import render

# Create your views here.
def allcourses(request):
    return render(request,'courses.html')